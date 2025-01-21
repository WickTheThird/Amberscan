import os
from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from .models import Images, ProcessedImage
from .tesseract import GoogleVisionOCR
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_image_task(image_path):
    try:
        logger.info(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")


        if image_path.startswith('./media'):
            image_path = image_path[len('./media/'):]

        if image_path.startswith(settings.MEDIA_ROOT):
            relative_path = os.path.relpath(image_path, settings.MEDIA_ROOT)
        else:
            relative_path = image_path

        full_image_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, relative_path))

        if not os.path.exists(full_image_path):
            raise FileNotFoundError(f"No such file or directory: '{full_image_path}'")

        ocr = GoogleVisionOCR(image_path=full_image_path)
        ocr_text = ocr.extract_text_from_image()
        if not ocr_text:
            raise ValueError(f"No text extracted for image at path {image_path}")

        processed_result = ocr.get_completion(ocr_text)
        if not processed_result:
            raise ValueError(f"Failed to process OCR data for image at path {image_path} {processed_result}")

        image = Images.objects.get(image=relative_path)
        with transaction.atomic():
            ProcessedImage.objects.create(
                user=image.client,
                image=image.id,
                company_name=processed_result.get("company_details", {}).get("name"),
                address=processed_result.get("company_details", {}).get("address"),
                vat_number=processed_result.get("company_details", {}).get("vat_number"),
                transaction_date=processed_result.get("transaction_details", {}).get("date"),
                transaction_time=processed_result.get("transaction_details", {}).get("time"),
                payment_method=processed_result.get("transaction_details", {}).get("payment_method"),
                items=processed_result.get("items"),
                fuel_type=processed_result.get("fuel_type"),
                is_invoice=processed_result.get("is_invoice"),
                total_gross=processed_result.get("totals", {}).get("total_gross"),
                total_vat=processed_result.get("totals", {}).get("total_vat"),
                total_net=processed_result.get("totals", {}).get("total_net"),
            )

        logger.info(f"Successfully processed image at path {image_path}")
        return {"image_path": image_path, "status": "success"}

    except FileNotFoundError as e:
        logger.error(str(e))
        return {"image_path": image_path, "status": "error", "error": str(e)}

    except Images.DoesNotExist:
        logger.error(f"Image not found in the database: {image_path}")
        return {"image_path": image_path, "status": "error", "error": "Image not found in database"}

    except Exception as e:
        logger.error(f"Error processing image at path {image_path}: {e}", exc_info=True)
        return {"image_path": image_path, "status": "error", "error": str(e)}
