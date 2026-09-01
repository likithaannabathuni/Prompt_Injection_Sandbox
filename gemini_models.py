import os
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()


# Get Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured in the .env file."
    )


# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Display available models
print("\nAvailable Gemini models:\n")

for model in client.models.list():

    print(model.name)