import asyncio
from google.cloud import vision
from google.oauth2 import service_account
from openai import OpenAI
import os

from .models import SecretKey

# from datetime import datetime
# from .models import ProcessedImage

os.environ["OPENAI_API_KEY"] = SecretKey.objects.get(user="openai").key

class GoogleVisionOCR:
    def __init__(self, credentials_path='./media/key/serious-cabinet-441714-j0-dbdb45c99a95.json'):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = vision.ImageAnnotatorClient(credentials=self.credentials)

    async def extract_text_from_image(self, image_path):
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = await asyncio.to_thread(self.client.text_detection, image=image)

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

    async def extract_text_from_pdf(self, pdf_path):
        """Handles PDF by converting pages to images and extracting text."""
        from PyPDF2 import PdfReader
        pdf_reader = PdfReader(pdf_path)
        tasks = []

        for page_number, page in enumerate(pdf_reader.pages):
            image_path = f"/tmp/page_{page_number}.png"
            page_image = page.to_image(resolution=300)  # Convert to image
            page_image.save(image_path)
            tasks.append(self.extract_text_from_image(image_path))

        return await asyncio.gather(*tasks)
    async def get_completion(self, ocr_text, model="gpt-4"):
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

        messages = [
            {"role": "system", "content": "You are Amberscan, a financial assistant for VAT compliance. Respond only in JSON."},
            {"role": "user", "content": prompt}
        ]

        client = OpenAI()
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content

    async def process_image(self, image_path):
        ocr_text = await self.extract_text_from_image(image_path)
        completion = await self.get_completion(ocr_text)
        return completion

    async def process_images_concurrently(self, image_paths):
        tasks = [self.process_image(path) for path in image_paths]
        return await asyncio.gather(*tasks)
