import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=GEMINI_API_KEY)

image_models = [
    "gemini-2.5-flash-image",
    "gemini-3-pro-image",
    "gemini-3-pro-image-preview",
    "gemini-3.1-flash-image",
    "gemini-3.1-flash-image-preview",
    "gemini-3.1-flash-lite-image",
    "nano-banana-pro-preview",
]

print("\nChecking available image-generation models...\n")

for model_name in image_models:
    try:
        model = client.models.get(model=model_name)

        print(f"✅ {model_name}")
        print(f"   Name: {model.name}")

    except Exception as e:
        print(f"❌ {model_name}")
        print(f"   {str(e)[:200]}")

    print()