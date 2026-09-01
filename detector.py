import os

from dotenv import load_dotenv
from groq import Groq


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# GROQ API KEY
# ==========================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured."
    )


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ==========================================
# PROMPT GUARD MODEL
# ==========================================

DETECTION_MODEL = "meta-llama/llama-prompt-guard-2-86m"


# ==========================================
# DETECTION
# ==========================================

def detect_prompt_injection(prompt):

    response = client.chat.completions.create(
        model=DETECTION_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=100
    )

    raw_result = response.choices[0].message.content.strip()

    # Convert model output to probability
    probability = float(raw_result)

    # Convert probability to percentage
    risk_score = probability * 100

    # ======================================
    # CLASSIFICATION
    # ======================================

    if risk_score < 40:

        classification = "SAFE"

    elif risk_score < 70:

        classification = "SUSPICIOUS"

    else:

        classification = "INJECTION"


    return {
        "probability": probability,
        "risk_score": risk_score,
        "classification": classification
    }