import streamlit as st

from image_generator import generate_image
from detector import detect_prompt_injection


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #64748B;
        margin-bottom: 25px;
    }

    .info-card {
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        background: #F8FAFC;
        margin-bottom: 25px;
    }

    .security-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        background: white;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        background: white;
        min-height: 140px;
    }

    .workflow-card {
        padding: 18px;
        border-radius: 14px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        min-height: 150px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎨 AI Image Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Generate AI images safely using prompt injection detection.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INFORMATION CARD
# ============================================================

st.markdown(
    """
    <div class="info-card">

    <h3>🛡️ Secure AI Image Generation</h3>

    <p>
    Your image prompt is first analyzed for potential prompt
    injection attacks. Only prompts classified as safe are
    sent to the image-generation system.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROMPT INPUT
# ============================================================

st.subheader("📝 Create Your Image")

prompt = st.text_area(
    "Image Prompt",
    placeholder=(
        "Describe the image you want to generate...\n\n"
        "Example: A futuristic cybersecurity laboratory "
        "with AI security monitors and glowing computers."
    ),
    height=180,
    label_visibility="collapsed"
)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = st.button(
    "🛡️ Check Prompt & Generate Image",
    use_container_width=True,
    type="primary"
)


# ============================================================
# GENERATION PROCESS
# ============================================================

if generate_button:

    # ========================================================
    # VALIDATE PROMPT
    # ========================================================

    if not prompt.strip():

        st.warning(
            "⚠️ Please enter an image prompt first."
        )

        st.stop()


    clean_prompt = prompt.strip()


    # ========================================================
    # STEP 1 — SECURITY ANALYSIS
    # ========================================================

    st.markdown(
        "### 🛡️ Step 1 — Security Analysis"
    )


    with st.spinner(
        "Analyzing your prompt for prompt injection..."
    ):

        try:

            detection_result = detect_prompt_injection(
                clean_prompt
            )

        except Exception as e:

            st.error(
                "❌ Prompt injection detection failed."
            )

            st.exception(e)

            st.stop()


    # ========================================================
    # GET DETECTION VALUES
    # ========================================================

    classification = detection_result.get(
        "classification",
        "UNKNOWN"
    )

    risk_score = detection_result.get(
        "risk_score",
        0
    )

    probability = detection_result.get(
        "probability",
        0
    )


    # ========================================================
    # SECURITY RESULTS
    # ========================================================

    st.markdown(
        '<div class="security-card">',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Risk Score",
            f"{risk_score:.2f}%"
        )


    with col2:

        st.metric(
            "Probability",
            f"{probability:.4f}"
        )


    with col3:

        st.metric(
            "Classification",
            classification
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # SAFE
    # ========================================================

    if classification == "SAFE":

        st.success(
            "🟢 Prompt classified as SAFE."
        )

        st.markdown(
            "The security check passed. "
            "Your prompt can proceed to image generation."
        )


    # ========================================================
    # SUSPICIOUS
    # ========================================================

    elif classification == "SUSPICIOUS":

        st.warning(
            "🟡 Prompt classified as SUSPICIOUS."
        )

        st.markdown(
            """
            This prompt may contain potentially unsafe
            instructions, so image generation has been stopped.
            """
        )

        st.info(
            "Try rewriting your prompt as a simple description "
            "of the image you want."
        )

        st.stop()


    # ========================================================
    # INJECTION
    # ========================================================

    elif classification == "INJECTION":

        st.error(
            "🔴 Prompt Injection Detected!"
        )

        st.markdown(
            """
            The prompt was blocked because the security model
            detected a high probability of prompt injection.
            """
        )

        st.warning(
            "Image generation was blocked for security reasons."
        )

        st.stop()


    # ========================================================
    # UNKNOWN
    # ========================================================

    else:

        st.error(
            "❌ Unable to classify the prompt."
        )

        st.stop()


    # ========================================================
    # STEP 2 — IMAGE GENERATION
    # ========================================================

    st.markdown(
        "### 🎨 Step 2 — Image Generation"
    )


    with st.spinner(
        "🤖 Generating your image..."
    ):

        image_result = generate_image(
            clean_prompt
        )


    # ========================================================
    # SUCCESS
    # ========================================================

    if image_result["success"]:

        provider = image_result.get(
            "provider",
            "AI"
        )


        st.success(
            f"✅ Image generated successfully using {provider}!"
        )


        image_data = image_result["image_data"]


        # ----------------------------------------------------
        # DISPLAY IMAGE
        # ----------------------------------------------------

        st.image(
            image_data,
            caption=f"Generated using {provider}",
            use_container_width=True
        )


        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        st.download_button(
            label="⬇️ Download Generated Image",
            data=image_data,
            file_name="generated_image.png",
            mime="image/png",
            use_container_width=True
        )


    # ========================================================
    # ALL PROVIDERS FAILED
    # ========================================================

    elif image_result["error_type"] == "ALL_PROVIDERS_FAILED":

        st.error(
            "❌ Image Generation Failed"
        )

        st.info(
            image_result["message"]
        )


    # ========================================================
    # OTHER ERROR
    # ========================================================

    else:

        st.error(
            "❌ Image generation failed."
        )

        st.info(
            image_result.get(
                "message",
                "Unable to generate the image."
            )
        )


# ============================================================
# SECURE WORKFLOW
# ============================================================

st.divider()

st.subheader(
    "🔐 Secure Image Generation Workflow"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="workflow-card">

        <h3>1️⃣ Enter Prompt</h3>

        <p>
        Describe the image you want the AI to create.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="workflow-card">

        <h3>2️⃣ Security Check</h3>

        <p>
        Prompt Guard analyzes the prompt for potential
        injection attacks.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="workflow-card">

        <h3>3️⃣ AI Generation</h3>

        <p>
        Safe prompts are sent to an available image-generation
        provider.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# EXAMPLES
# ============================================================

st.divider()

st.subheader(
    "💡 Example Prompts"
)


examples = [
    "A futuristic AI cybersecurity laboratory",
    "A professional AI research center with advanced computers",
    "A cyber security robot protecting an AI system",
    "A futuristic computer network security center",
    "An artificial intelligence security dashboard"
]


for example in examples:

    st.markdown(
        f"• `{example}`"
    )


# ============================================================
# FEATURES
# ============================================================

st.divider()

st.subheader(
    "🚀 Features"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="feature-card">

        <h3>🛡️ Secure</h3>

        <p>
        Prompts are checked for prompt injection attacks
        before image generation.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="feature-card">

        <h3>🤖 AI Powered</h3>

        <p>
        Uses Gemini with an automatic fallback image provider.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="feature-card">

        <h3>⬇️ Download</h3>

        <p>
        Generated images can be downloaded as PNG files.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🛡️ Prompt Injection Sandbox • Secure AI Image Generation"
)