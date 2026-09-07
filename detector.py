import os
import re

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GROQ API KEY
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# PROMPT GUARD MODEL
# ============================================================

DETECTION_MODEL = (
    "meta-llama/llama-prompt-guard-2-86m"
)


# ============================================================
# DETECTION FUNCTION
# ============================================================

def detect_prompt_injection(text):
    """
    Detect possible prompt injection.

    Returns:
        {
            "probability": float,
            "risk_score": float,
            "classification": "SAFE" | "SUSPICIOUS" | "INJECTION",
            "raw_result": str
        }
    """

    # --------------------------------------------------------
    # EMPTY TEXT
    # --------------------------------------------------------

    if not text or not text.strip():

        return {
            "probability": 0.0,
            "risk_score": 0.0,
            "classification": "SAFE",
            "raw_result": ""
        }


    # --------------------------------------------------------
    # LIMIT INPUT
    # --------------------------------------------------------

    text = text[:12000]


    try:

        # ----------------------------------------------------
        # CALL PROMPT GUARD
        # ----------------------------------------------------

        response = client.chat.completions.create(

            model=DETECTION_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ],

            temperature=0,

            max_tokens=20
        )


        # ----------------------------------------------------
        # GET RAW RESPONSE
        # ----------------------------------------------------

        raw_result = (
            response
            .choices[0]
            .message
            .content
        )


        if raw_result is None:

            raw_result = ""


        raw_result = raw_result.strip()

        normalized = raw_result.lower().strip()


        # ====================================================
        # NUMERIC OUTPUT
        # ====================================================

        # Supports:
        #
        # 0.05
        # 0.95
        # 5
        # 95
        # risk: 0.8
        # probability: 85%
        #

        number_match = re.search(
            r"[-+]?\d*\.?\d+",
            normalized
        )


        if number_match:

            probability = float(
                number_match.group()
            )


            # ------------------------------------------------
            # HANDLE PERCENTAGE
            # ------------------------------------------------

            if probability > 1:

                probability = probability / 100


            probability = max(
                0.0,
                min(
                    probability,
                    1.0
                )
            )


            risk_score = (
                probability * 100
            )


            # ------------------------------------------------
            # CLASSIFICATION
            # ------------------------------------------------

            if risk_score < 40:

                classification = "SAFE"


            elif risk_score < 70:

                classification = "SUSPICIOUS"


            else:

                classification = "INJECTION"


            return {

                "probability": round(
                    probability,
                    4
                ),

                "risk_score": round(
                    risk_score,
                    2
                ),

                "classification": classification,

                "raw_result": raw_result
            }


        # ====================================================
        # LABEL OUTPUT
        # ====================================================

        # ----------------------------------------------------
        # SAFE LABELS
        # ----------------------------------------------------

        safe_keywords = [

            "benign",

            "safe",

            "clean",

            "not_injection",

            "not injection",

            "no injection"

        ]


        if any(
            keyword in normalized
            for keyword in safe_keywords
        ):

            return {

                "probability": 0.05,

                "risk_score": 5.0,

                "classification": "SAFE",

                "raw_result": raw_result
            }


        # ----------------------------------------------------
        # INJECTION LABELS
        # ----------------------------------------------------

        injection_keywords = [

            "prompt injection",

            "prompt_injection",

            "jailbreak",

            "malicious",

            "injection detected",

            "unsafe"

        ]


        if any(
            keyword in normalized
            for keyword in injection_keywords
        ):

            return {

                "probability": 0.95,

                "risk_score": 95.0,

                "classification": "INJECTION",

                "raw_result": raw_result
            }


        # ----------------------------------------------------
        # SUSPICIOUS LABELS
        # ----------------------------------------------------

        suspicious_keywords = [

            "suspicious",

            "potentially malicious",

            "possible injection",

            "possibly unsafe"

        ]


        if any(
            keyword in normalized
            for keyword in suspicious_keywords
        ):

            return {

                "probability": 0.60,

                "risk_score": 60.0,

                "classification": "SUSPICIOUS",

                "raw_result": raw_result
            }


        # ====================================================
        # UNKNOWN OUTPUT
        # ====================================================
        #
        # We do not automatically mark unknown output as
        # suspicious, because that was causing normal PDFs
        # to become SUSPICIOUS.
        #
        # ====================================================

        return {

            "probability": 0.10,

            "risk_score": 10.0,

            "classification": "SAFE",

            "raw_result": raw_result
        }


    except Exception as e:

        # ----------------------------------------------------
        # API ERROR
        # ----------------------------------------------------

        return {

            "probability": 0.0,

            "risk_score": 0.0,

            "classification": "SAFE",

            "raw_result": "",

            "error": str(e)
        }