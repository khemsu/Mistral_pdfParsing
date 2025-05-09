# import os
# from mistralai import Mistral
# import requests
# from dotenv import load_dotenv


# load_dotenv()
# api_key = os.environ["MISTRAL_API_KEY"]

# pdf_path = "Shift001.pdf"

# model = "mistral-small-latest"
# client = Mistral(api_key=api_key)

# if not os.path.exists(pdf_path):
#     print(f"File not found: {pdf_path}")
#     exit()


# with open(pdf_path, "rb") as f:
#     uploaded_pdf = client.files.upload(
#         file={
#             "file_name": os.path.basename(pdf_path),
#             "content": f,
#         },
#         purpose="ocr"
#     )

# signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

# messages = [
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "text",
#                 "text": "You are an intellegient document parser, and your role is to extract the text from the pdf below as you read naturally maintaing the structure. Do not hallucinate."
#             },
#             {
#                 "type": "document_url",
#                 "document_url": signed_url.url
#             }
#         ]
#     }
# ]

# chat_response = client.chat.complete(
#         model=model,
#         messages=messages
#     )

# print("Raw text.")
# print(chat_response.choices[0].message.content)
