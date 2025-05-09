import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]

pdf_path = "pdf/B.K.pdf"    #pdf path heree
client = Mistral(api_key=api_key)

model="mistral-small-latest"

def extract_raw_text_from_pdf(file_path):
    """Uploads the PDF and extracts raw text using Mistral."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "rb") as f:
        uploaded_pdf = client.files.upload(
            file={
                "file_name": os.path.basename(file_path),
                "content": f,
            },
            purpose="ocr"
        )

    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You are an intelligent document parser, and your role is to extract the text from the PDF below as you read naturally. Do not hallucinate."
                },
                {
                    "type": "document_url",
                    "document_url": signed_url.url
                }
            ]
        }
    ]

    chat_response = client.chat.complete(
        model= model,
        messages=messages
    )

    return chat_response.choices[0].message.content

def extract_vendor_details(raw_text):

    messages = [
        {
            "role": "user",
            "content": f"""You are an expert document parser specializing in commercial documents like invoices, bills, etc.Extract the following structured data from the document text:
                - vendor_details: name, address, phone, email, website, PAN
                - customer_details: name, address, contact, PAN (usually below vendor_details)
                - invoice_details: bill_number, bill_date, transaction_date, mode_of_payment, finance_manager, authorized_signatory
                - payment_details: total, in_words, discount, taxable_amount, vat, net_amount
                - line_items (list): hs_code, description, qty, rate, amount
                    Rules:
                        1. Extract only the fields listed; do not guess or add extra fields.
                        2. If a field is missing, set its value as null.
                        3. Use context ('Vendor', 'Supplier', 'Bill To', 'Customer', etc.) to distinguish parties. If unclear, the first business is Vendor,                        the second is Customer.
                        4. Each line_item must include hs_code and description; qty, rate, and amount are optional.
                        5. Always return the result strictly in the following JSON structure.
                        6. PAN numbers are typically boxed or near labels like 'PAN No.', and follow a 9-digit (Nepal) format.

                        Return the structured data using this exact JSON format:
                        {{
                            "vendor_details": {{
                              "name": "...",
                              "address": "...", 
                              "phone": "...", 
                              "email": "...",
                              "website": "...",
                              "pan": "..."
                            }},
                            "customer_details": {{
                                "name": "...",
                                "address": "...",
                                "contact": "...",
                                "pan": "..."
                              }},
                              "invoice_details": {{
                                "bill_number": "...",
                                "bill_date": "...",
                                "transaction_date": "...",
                                "mode_of_payment": "...",
                                "finance_manager": "...",
                                "authorized_signatory": "..."
                              }},
                              "payment_details": {{
                                "total": 0,
                                "in_words": "...",
                                "discount": 0,
                                "taxable_amount": 0,
                                "vat": 0,
                                "net_amount": 0
                              }},
                              "line_items": [
                                {{
                                  "hs_code": "...",
                                  "particulars": "...",
                                  "qty": "...",
                                  "rate": "...",
                                  "amount": "..."
                                }}
                              ]
                            }}

                            Text:
                            {raw_text}

                            Important: Return ONLY the JSON object. No explanations, no headings, no extra text.
"""
        }
    ]
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content


try:
    raw_text = extract_raw_text_from_pdf(pdf_path)
    print("Raw Text Extraction here..")
    print(raw_text)

    key_info= extract_vendor_details(raw_text)
    print("\nExtracting key Details:")
    print(key_info)

except Exception as e:
    print(f"Error: {e}")
