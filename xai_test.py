import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("XAI_API_KEY")

if not api_key:
    raise ValueError("XAI_API_KEY is not configured.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1"
)

print("Testing xAI connection...")

models = client.models.list()

print("\nModels available:\n")

for model in models.data:
    print(model.id)