import base64
import hashlib
import hmac
import asyncio
from asgiref.sync import sync_to_async

import logging
logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.contrib.auth import login, logout
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login

from .serializers import SerializeLoginClient, SerializeSignInClient, SerializeImages, SerializePDF
from .models import Images, PDFs, Providers, ProcessedImage
from .tesseract import GoogleVisionOCR
from .tasks import process_image_task



SECRET_KEY = settings.SECRET_KEY
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in Django settings.")


# Signature Functions
def sign(username):
    try:
        hmac_obj = hmac.new(SECRET_KEY.encode(), username.encode(), hashlib.sha256)
        signature = base64.urlsafe_b64encode(hmac_obj.digest()).decode('utf-8')
        return signature
    except Exception as e:
        logger.error(f"Error generating signature for {username}: {e}")
        raise


def verify_signature(username, signature):
    expected_signature = sign(username)
    return hmac.compare_digest(expected_signature, signature)


# API Views
class LogIn(APIView):
    def post(self, request):
        serializer = SerializeLoginClient(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                provider, created = Providers.objects.get_or_create(
                    client=user,
                    defaults={
                        "signature": sign(user.username),
                        "created_at": now(),
                        "last_used_at": now(),
                    },
                )

                if not created:
                    provider.signature = sign(user.username)
                    provider.last_used_at = now()
                    provider.save()

                return Response(
                    status=status.HTTP_201_CREATED,
                    data={"signature": provider.signature}
                )
            else:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={"error": "Invalid credentials"}
                )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )


class Permissions(APIView):
    def get(self, request):
        signature = request.headers.get("Authorization", "").replace("Bearer ", "").strip()

        if not signature:
            return Response({"error": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            provider = Providers.objects.get(signature=signature, is_active=True)
            provider.last_used_at = now()
            provider.save()
        except Providers.DoesNotExist:
            return Response({"error": "Invalid or expired signature"}, status=status.HTTP_401_UNAUTHORIZED)

        user = provider.client
        is_admin = user.is_staff

        return Response(
            {
                "username": user.username,
                "email": user.email,
                "is_admin": is_admin,
            },
            status=status.HTTP_200_OK,
        )


class RegisterClient(APIView):
    def post(self, request):
        serializer = SerializeSignInClient(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            signature = sign(user.username)
            return Response(status=status.HTTP_201_CREATED, data={"signature": signature})

        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if session_key:
            try:
                session = Session.objects.get(session_key=session_key)
                session.delete()
            except Session.DoesNotExist:
                pass

        logout(request)
        return Response({
            "message": "Logout successful. Your session has been terminated."
        }, status=status.HTTP_200_OK)


class Images(APIView):
    def post(self, request):
        is_bulk = isinstance(request.data, list)
        serializer = SerializeImages(data=request.data, many=is_bulk)

        if serializer.is_valid():
            saved_data = serializer.save()

            image_objects = saved_data if is_bulk else [saved_data]
            results = []

            for image in image_objects:
                task = process_image_task.delay(image.image.path)
                results.append({"image_path": image.image.path, "task_id": task.id})

            return Response(
                {
                    "message": "Images uploaded successfully. Processing has started.",
                    "tasks": results,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        username = request.query_params.get('username')
        signature = request.query_params.get('signature')

        if not username or not signature:
            return Response({"error": "Username and signature are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not verify_signature(username, signature):
            return Response({"error": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)

        images = Images.objects.filter(client__username=username)
        serializer = SerializeImages(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        image_id = request.query_params.get('id')
        if not image_id:
            return Response({"error": "Image ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Images.objects.get(id=image_id)
            image.delete()
            return Response({"message": "Image deleted successfully"}, status=status.HTTP_200_OK)
        except Images.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        image_id = request.query_params.get('id')
        if not image_id:
            return Response({"error": "Image ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Images.objects.get(id=image_id)
            serializer = SerializeImages(image, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Images.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)



class PDFs(APIView):
    def post(self, request):
        serializer = SerializePDF(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        pdfs = PDFs.objects.all()
        serializer = SerializePDF(pdfs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        pdf_id = request.query_params.get('id')
        if not pdf_id:
            return Response({"error": "PDF ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = PDFs.objects.get(id=pdf_id)
            pdf.delete()
            return Response({"message": "PDF deleted successfully"}, status=status.HTTP_200_OK)
        except PDFs.DoesNotExist:
            return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        pdf_id = request.query_params.get('id')
        if not pdf_id:
            return Response({"error": "PDF ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pdf = PDFs.objects.get(id=pdf_id)
            serializer = SerializePDF(pdf, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PDFs.DoesNotExist:
            return Response({"error": "PDF not found"}, status=status.HTTP_404_NOT_FOUND)

    # async def process_pdfs(self, pdf_objects):
    #     ocr = GoogleVisionOCR()
    #     tasks = [ocr.extract_text_from_pdf(pdf.pdf.path) for pdf in pdf_objects]
    #     pdf_texts = await asyncio.gather(*tasks)

    #     results = []
    #     for pdf_obj, pages_text in zip(pdf_objects, pdf_texts):
    #         full_text = "\n".join(pages_text)
    #         processed_result = await ocr.get_completion(full_text)
    #         processed_image = ProcessedImage.objects.create(
    #             user=pdf_obj.client,
    #             pdf=pdf_obj,
    #             company_name=processed_result.get("company_details", {}).get("name"),
    #             address=processed_result.get("company_details", {}).get("address"),
    #             vat_number=processed_result.get("company_details", {}).get("vat_number"),
    #             transaction_date=processed_result.get("transaction_details", {}).get("date"),
    #             transaction_time=processed_result.get("transaction_details", {}).get("time"),
    #             payment_method=processed_result.get("transaction_details", {}).get("payment_method"),
    #             items=processed_result.get("items"),
    #             fuel_type=processed_result.get("fuel_type"),
    #             is_invoice=processed_result.get("is_invoice"),
    #             total_gross=processed_result.get("totals", {}).get("total_gross"),
    #             total_vat=processed_result.get("totals", {}).get("total_vat"),
    #             total_net=processed_result.get("totals", {}).get("total_net"),
    #         )
    #         results.append(processed_image)

    #     return results
