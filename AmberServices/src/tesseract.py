import cv2
import numpy as np
from PIL import Image
from google.cloud import vision
from google.oauth2 import service_account
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from openai import OpenAI
import time
import os
import asyncio

key: str = ''
with open('./media/key/open_cabinet.txt') as f: key = f.read()

os.environ["OPENAI_API_KEY"] = key

class GoogleVisionOCR:
    def __init__(self, credentials_path='./media/key/serious-cabinet-441714-j0-dbdb45c99a95.json'):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = vision.ImageAnnotatorClient(credentials=self.credentials)

    def extract_text_from_image(self, image_path):

        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(f"Error with Google Vision API: {response.error.message}")

        full_text = response.full_text_annotation.text
        return full_text


    #! EXPERIMENTAL
    def slice_image_on_maximum_peak(self, image_path, edge_margin=50):
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            edges = cv2.Canny(blurred, 50, 150)

            vertical_projection = np.sum(edges, axis=0)

            vertical_projection[:edge_margin] = 0
            vertical_projection[-edge_margin:] = 0

            plt.plot(vertical_projection)
            plt.title("Modified Vertical Projection Profile (with Edges Ignored)")
            plt.xlabel("Column Index")
            plt.ylabel("Sum of Edge Intensity")
            plt.show()

            max_peak_index = np.argmax(vertical_projection)

            boundaries = [0, max_peak_index, len(vertical_projection) - 1]

            slices = []
            for i in range(len(boundaries) - 1):
                start = boundaries[i]
                end = boundaries[i + 1]
                if end - start > 50:
                    sliced_img = img[:, start:end]
                    slices.append(sliced_img)
                    cv2.imwrite(f"sliced_receipt_{i}.jpg", sliced_img)

            return slices

    #! EXPERIMENTAL
    def slice_image_on_vertical_lines(self, image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blurred, 50, 150)

        vertical_projection = np.sum(edges, axis=0)

        plt.plot(vertical_projection)
        plt.title("Vertical Projection")
        plt.xlabel("Column Index")
        plt.ylabel("Sum of Edge Intensity")
        plt.show()

        threshold = np.max(vertical_projection) * 0.15
        vertical_gaps = vertical_projection < threshold

        min_gap_width = 50

        vertical_boundaries = []
        start = None

        for i, is_gap in enumerate(vertical_gaps):
            if is_gap:
                if start is None:
                    start = i
            else:
                if start is not None:
                    if i - start >= min_gap_width:
                        vertical_boundaries.append((start, i))
                    start = None

        slices = []
        for i, (start, end) in enumerate(vertical_boundaries):
            if end - start > min_gap_width:
                sliced_img = img[:, start:end]
                slices.append(sliced_img)
                cv2.imwrite(f"sliced_receipt_{i}.jpg", sliced_img)

        if not slices:
            print("No suitable gaps detected. Try adjusting threshold or min_gap_width.")
        
        return slices

    def get_completion(self, data, model="gpt-4o", image_url=None):

        prompt = f"""
        You are an advanced AI assistant named **Amberscan**, specialized in extracting, interpreting, and calculating financial information from receipts and invoices. Based on the provided data, your tasks are as follows:

        ### 1. Data Extraction:
        Parse the input text to identify and extract:
        - **Company Details**:
        - Name, address, and VAT number (if available).
        - **Transaction Details**:
        - Date and time of the transaction.
        - Payment method (e.g., cash, credit card, or other details).
        - **Purchased Items**:
        - Item descriptions.
        - Quantities (if specified).
        - Unit prices and total prices for each item.

        ### 2. VAT Classification and Calculation:
        Using Irish VAT laws, classify each item and calculate its tax components:
        - **VAT Rates**:
        - 0% for specific essential goods (e.g., bread, milk, children's clothing).
        - 9% for hospitality, newspapers, and certain cultural activities.
        - 13.5% for heating fuels, renovations, and some construction services.
        - 23% as the standard VAT rate for most goods and services.
        - Default to 23% if the item's category is unclear.

        - For each item, compute:
        - **Gross Price**: Total price (including VAT).
        - **VAT Amount**, calculated as:
            VAT Amount = Gross Price × (VAT Rate / (100 + VAT Rate))
        - **Net Price**, calculated as:
            Net Price = Gross Price - VAT Amount.

        ### 3. Tax Deductibility:
        Identify whether each item is eligible for VAT deduction under Irish tax law. Examples:
        - **Not Eligible**:
        - Items for personal use or consumption.
        - Certain entertainment expenses.
        - **Eligible**:
        - Goods or services for business purposes (e.g., fuel for commercial vehicles).

        ### 4. JSON Output:
        Summarize all extracted and calculated information in a structured JSON format:
        - **Company Information**:
        - Name, address, VAT number.
        - **Transaction Information**:
        - Date, time, and payment method.
        - **Items** (for each item):
        - Description.
        - Quantity.
        - Unit price (if applicable).
        - Gross price.
        - VAT rate.
        - VAT amount.
        - Net price.
        - Whether the item is tax-deductible.
        - **Totals**:
        - Total gross amount.
        - Total VAT amount.
        - Total net amount.
        - **Additional Flags**:
        - If the document is an invoice, set "is_invoice": true.
        - If data is incomplete (e.g., missing VAT number or quantities), set missing fields to `null`.

        ### Example JSON Output:
        ```json
        {{
        "company_name": "CIRCLE K",
        "company_address": "Elm Park Service Station, Merion Road, Dublin 4",
        "vat_number": "IE8204169W",
        "date": "2023-06-08",
        "time": "08:04",
        "items": [
            {{
            "description": "RED BULL 250ML",
            "quantity": 1,
            "gross_price": 7.50,
            "vat_rate": 23,
            "vat_amount": 1.40,
            "net_price": 6.10,
            "tax_deductible": false
            }},
            {{
            "description": "Diesel",
            "quantity": 48.47,
            "price_per_unit": 1.509,
            "gross_price": 73.14,
            "vat_rate": 23,
            "vat_amount": 13.68,
            "net_price": 59.46,
            "tax_deductible": true
            }}
        ],
        "total_net_amount": 65.56,
        "total_vat_amount": 15.08,
        "total_gross_amount": 80.64,
        "payment_method": "Visa XXXX XXXX XXXX 9051",
        "is_invoice": false
        }}
        ```

        ### 5. Error Handling and Validation:
        - Ensure all calculations are accurate to two decimal places.
        - Flag inconsistencies or ambiguous data for review, and include a brief explanation in the JSON output.

        ---
        **Data Input**: {data}
        """

        messages = [
            {"role": "system", "content": "You are Amberscan, a financial assistant for VAT compliance and receipt analysis."},
            {"role": "user", "content": prompt}
        ]

        client = OpenAI()
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            files=[image_url] if image_url else None,
            temperature=1.00,
            top_p=1.00,
            response_format={ "type": "json_object" }
            )

        return response.choices[0].message.content



#! Testing reading
# ocr = GoogleVisionOCR()
# image_path = "../media/test2_6.png"
# # image_path = "../media/test5.png"
# receipt_data = ocr.extract_text_from_image(image_path)
# response = ocr.get_completion(receipt_data)
# print(response)

#! Testing splitting

# lines_of_text = ocr.extract_lines_from_image(image_path)
# lines_of_text = ocr.slice_image_on_maximum_peak(image_path)

# for i, line in enumerate(lines_of_text, start=1):
#     print(f"Line {i}: {line}")


# # Slice the image based on detected vertical gaps
# sliced_images = ocr.slice_image_on_vertical_lines(image_path)

# # If you need to display each slice
# for idx, slice_img in enumerate(sliced_images):
#     pil_img = Image.fromarray(slice_img)
#     pil_img.show()
