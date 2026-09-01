import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)

image_path = r"C:\Users\91812\Downloads\test_image.jpg"

image = Image.open(image_path)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Describe this image in detail. What is shown in the image?",
        image
    ]
)

print("\n========== GEMINI IMAGE ANSWER ==========\n")
print(response.text)