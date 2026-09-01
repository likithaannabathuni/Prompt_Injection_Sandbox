import os
import urllib.parse

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import errors


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GEMINI API KEY
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured in the .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# IMAGE MODELS
# ============================================================

IMAGE_MODEL = "gemini-3.1-flash-image"


# ============================================================
# POLLINATIONS API
# ============================================================

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/"


# ============================================================
# GEMINI IMAGE GENERATION
# ============================================================

def generate_with_gemini(prompt):

    try:

        response = client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt
        )

        if not response.candidates:
            return None

        for candidate in response.candidates:

            if not candidate.content:
                continue

            for part in candidate.content.parts:

                if hasattr(part, "inline_data"):

                    if part.inline_data:

                        return part.inline_data.data

        return None

    except errors.ClientError:
        return None

    except Exception:
        return None


# ============================================================
# POLLINATIONS IMAGE GENERATION
# ============================================================

def generate_with_pollinations(prompt):

    try:

        # Encode prompt safely for URL
        encoded_prompt = urllib.parse.quote(
            prompt,
            safe=""
        )

        # Build URL
        url = (
            POLLINATIONS_URL
            + encoded_prompt
            + "?width=1024"
            + "&height=1024"
            + "&nologo=true"
        )

        # Request image
        response = requests.get(
            url,
            timeout=120
        )

        # Check response
        if response.status_code == 200:

            if response.content:

                return response.content

        return None

    except requests.RequestException:

        return None

    except Exception:

        return None


# ============================================================
# MAIN IMAGE GENERATION FUNCTION
# ============================================================

def generate_image(prompt):

    # ========================================================
    # STEP 1 — TRY GEMINI
    # ========================================================

    gemini_image = generate_with_gemini(
        prompt
    )

    if gemini_image:

        return {
            "success": True,
            "image_data": gemini_image,
            "provider": "Gemini",
            "error_type": None,
            "message": (
                "Image generated successfully using Gemini."
            )
        }


    # ========================================================
    # STEP 2 — GEMINI UNAVAILABLE
    # ========================================================

    # Gemini may be unavailable because of quota,
    # billing, rate limits, or another API problem.


    # ========================================================
    # STEP 3 — TRY FALLBACK
    # ========================================================

    pollinations_image = generate_with_pollinations(
        prompt
    )

    if pollinations_image:

        return {
            "success": True,
            "image_data": pollinations_image,
            "provider": "Pollinations",
            "error_type": None,
            "message": (
                "Gemini was unavailable. "
                "Image generated using the fallback provider."
            )
        }


    # ========================================================
    # STEP 4 — BOTH FAILED
    # ========================================================

    return {
        "success": False,
        "image_data": None,
        "provider": None,
        "error_type": "ALL_PROVIDERS_FAILED",
        "message": (
            "Both Gemini and the fallback image-generation "
            "service are currently unavailable."
        )
    }