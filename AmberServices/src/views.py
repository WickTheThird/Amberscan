from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from .serializers import *
from .tesseract import *
from .auth import sign

#NOTE -> placehoder
def index(request):
    return None

#! Authentication
class LogIn(APIView):

    def post(self, request):
        
        serialiser = SerializeLoginClient(data=request.data)
        
        if serialiser.is_valid():
            
            user = authenticate(username=serialiser.validated_data['email'], password=serialiser.validated_data['password'])
            
            if user is not None:
                
                # CREATE A HTTTP SIGNATURE
                
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterClient(APIView):

    def post(self, request):

        serializer = SerializeSignInClient(data=request.data) # The check for the fields is done by the serialsier

        if serializer.is_valid():

            signature = sign(request.data.username)

            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)


def logout(self, request): # TODO: we need to check if the user has a session aleardy but this could be !optional!
    logout(request)
    return Response(status=status.HTTP_200_OK)

#! API
class Images(APIView):
    
    def post(self, request):
        pass
    def get(self, request):
        pass
    def delete(self, request):
        pass
    def put(self, request):
        pass


class PDFs(APIView):
    
    def post(self, request):
        pass
    
    def get(self, request):
        pass
    
    def delete(self, request):
        pass
    
    def put(self, request):
        pass
