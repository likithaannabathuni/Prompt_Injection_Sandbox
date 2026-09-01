import streamlit as st

from style import apply_custom_style
from llm import generate_response, MODEL_NAME
from detector import detect_prompt_injection
from database import get_connection


apply_custom_style()


# ==========================================
# PAGE PROTECTION
# ==========================================

if not st.session_state.get(
    "logged_in",
    False
):

    st.switch_page(
        "pages/authentication.py"
    )


# ==========================================
# HEADER
# ==========================================

st.title("🧪 Prompt Injection Testing")

st.write(
    "Test prompts against an LLM and analyze "
    "possible prompt injection attacks."
)


# ==========================================
# MODEL CARDS
# ==========================================

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        f"""
        <div class="color-card">

        <h3>🤖 Main LLM</h3>

        <p>{MODEL_NAME}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="color-card">

        <h3>🛡️ Security Detector</h3>

        <p>Meta Prompt Guard</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# PROMPT
# ==========================================

st.subheader("📝 Enter Prompt")

prompt = st.text_area(
    "Prompt",
    height=200,
    placeholder=(
        "Enter a prompt to test..."
    )
)


# ==========================================
# TEST
# ==========================================

if st.button(
    "🚀 Analyze & Test Prompt",
    use_container_width=True
):

    if not prompt.strip():

        st.warning(
            "Please enter a prompt."
        )

    else:

        clean_prompt = prompt.strip()

        # ======================================
        # DETECTION
        # ======================================

        with st.spinner(
            "🛡️ Analyzing prompt..."
        ):

            try:

                detection = detect_prompt_injection(
                    clean_prompt
                )

            except Exception as e:

                st.error(
                    f"Detection error: {e}"
                )

                st.stop()


        classification = detection[
            "classification"
        ]

        risk_score = detection[
            "risk_score"
        ]

        probability = detection[
            "probability"
        ]


        # ======================================
        # SECURITY RESULT
        # ======================================

        st.subheader(
            "🛡️ Security Analysis"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            if classification == "SAFE":

                st.success(
                    "🟢 SAFE"
                )

            elif classification == "SUSPICIOUS":

                st.warning(
                    "🟡 SUSPICIOUS"
                )

            else:

                st.error(
                    "🔴 INJECTION"
                )


        with col2:

            st.metric(
                "Risk Score",
                f"{risk_score:.2f}/100"
            )


        with col3:

            st.metric(
                "Probability",
                f"{probability:.4f}"
            )


        st.progress(
            min(
                max(
                    int(risk_score),
                    0
                ),
                100
            )
        )


        # ======================================
        # RESPONSE
        # ======================================

        if classification == "INJECTION":

            st.markdown(
                """
                <div class="danger-card">

                <h3>🚨 Prompt Injection Detected</h3>

                <p>
                This prompt has a high probability
                of being a prompt injection attack.
                </p>

                <p>
                The prompt was blocked and was not
                sent to the main LLM.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            llm_response = (
                "Request blocked because a high-risk "
                "prompt injection was detected."
            )


        elif classification == "SUSPICIOUS":

            st.markdown(
                """
                <div class="warning-card">

                <h3>🟡 Suspicious Prompt</h3>

                <p>
                This prompt contains characteristics
                associated with prompt manipulation.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            with st.spinner(
                "🤖 Generating LLM response..."
            ):

                llm_response = generate_response(
                    clean_prompt
                )


        else:

            st.markdown(
                """
                <div class="safe-card">

                <h3>🟢 Prompt Appears Safe</h3>

                <p>
                No significant prompt injection
                indicators were detected.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            with st.spinner(
                "🤖 Generating LLM response..."
            ):

                llm_response = generate_response(
                    clean_prompt
                )


        # ======================================
        # LLM RESPONSE
        # ======================================

        st.divider()

        st.subheader("🤖 LLM Response")

        st.markdown(
            f"""
            <div class="color-card">

            {llm_response}

            </div>
            """,
            unsafe_allow_html=True
        )


        # ======================================
        # SAVE
        # ======================================

        try:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO test_results
                (
                    user_id,
                    prompt_text,
                    llm_response,
                    detection_result,
                    risk_score,
                    model
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    st.session_state.user_id,
                    clean_prompt,
                    llm_response,
                    classification,
                    risk_score,
                    MODEL_NAME
                )
            )

            conn.commit()
            conn.close()

            st.success(
                "✅ Test result saved successfully!"
            )

        except Exception as e:

            st.warning(
                f"Result could not be saved: {e}"
            )