import logging
from celery import shared_task
from google.cloud import vision
from google.oauth2 import service_account
from .models import SecretKey
import os
import aiofiles
from asgiref.sync import sync_to_async
from django.db import transaction

logging.basicConfig(level=logging.INFO)

@shared_task
def set_openai_key():
    try:
        secret_key = SecretKey.objects.get(user="openai")
        os.environ["OPENAI_API_KEY"] = secret_key.key
        logging.info("OpenAI API key set successfully.")
    except Exception as e:
        logging.error(f"Failed to set OpenAI API key: {e}")
        raise RuntimeError("Could not set OpenAI API key.")

set_openai_key.delay()


class GoogleVisionOCR:
    def __init__(self, credentials_path='./media/key/serious-cabinet-441714-j0-dbdb45c99a95.json'):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = vision.ImageAnnotatorClient(credentials=self.credentials)

    @shared_task
    def extract_text_from_image(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = self.client.text_detection(image=image)

            if response.error.message:
                raise Exception(f"Error with Google Vision API: {response.error.message}")

            ascii_text = "\n"
            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        line = []
                        for word in paragraph.words:
                            word_text = "".join(symbol.text for symbol in word.symbols)
                            line.append(word_text)
                        paragraph_text = " ".join(line)
                        ascii_text += f"{paragraph_text[:41].ljust(41)}\n"

            return ascii_text
        except Exception as e:
            logging.error(f"Failed to process image {image_path}: {e}")
            return None

    @shared_task
    def get_completion(self, ocr_text, model="gpt-4"):
        prompt = f"""
        You are Amberscan, an advanced AI for analyzing receipts and invoices under Irish tax laws. Your task is to:
        1. Extract and organize receipt details:
            - Identify the **company name**, address, and VAT number.
            - Extract **transaction details**: date, time, payment method.
            - Identify **items**: description, quantity, unit price, gross price.
            - Identify **fuel type** (e.g., Diesel, Petrol) if applicable.
            - Determine if the receipt is an invoice by checking for the exact words "invoice," "bill," or "bill number."
        2. Perform VAT calculations using Irish rates:
            - Assign appropriate VAT rates (0%, 9%, 13.5%, 23%).
            - Calculate gross, VAT, and net amounts for each item.
        3. Flag items as tax-deductible (`true` or `false`) based on Irish laws.
        4. Output results as JSON:
        {{
            "company_details": {{
                "name": "Company Name",
                "address": "Company Address",
                "vat_number": "VAT123456"
            }},
            "transaction_details": {{
                "date": "YYYY-MM-DD",
                "time": "HH:MM",
                "payment_method": "Cash/Card"
            }},
            "items": [...],
            "fuel_type": "Diesel/Petrol/None",
            "is_invoice": true,
            "totals": {{
                "total_gross": 100.00,
                "total_vat": 18.70,
                "total_net": 81.30
            }}
        }}
        ---
        Receipt Data:
        {ocr_text}
        """
        try:
            from openai import OpenAI  # Lazy import to avoid blocking Celery workers
            client = OpenAI()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are Amberscan, a financial assistant for VAT compliance. Respond only in JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Failed to get completion: {e}")
            return None

    @shared_task
    def process_image(self, image_path):
        try:
            ocr_text = GoogleVisionOCR.extract_text_from_image(image_path)
            if ocr_text:
                return GoogleVisionOCR.get_completion(ocr_text)
            return None
        except Exception as e:
            logging.error(f"Failed to process image {image_path}: {e}")
            return None

    @shared_task
    def process_images_concurrently(self, image_paths):
        results = []
        for path in image_paths:
            result = GoogleVisionOCR.process_image.delay(path)
            results.append(result)
        return results
