import streamlit as st

from style import apply_custom_style
from detector import detect_prompt_injection


apply_custom_style()


# ==========================================
# PROTECTION
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

st.title("🛡️ Prompt Injection Detection")

st.write(
    "Analyze a prompt using Meta Prompt Guard "
    "without sending it to the main LLM."
)


# ==========================================
# INFO
# ==========================================

st.markdown(
    """
    <div class="gradient-card">

    <h2>🔍 Security Scanner</h2>

    <p>
    Enter a prompt below to estimate its
    prompt injection probability.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# INPUT
# ==========================================

prompt = st.text_area(
    "📝 Prompt to Analyze",
    height=200,
    placeholder="Enter a prompt..."
)


# ==========================================
# ANALYZE
# ==========================================

if st.button(
    "🔍 Analyze Prompt",
    use_container_width=True
):

    if not prompt.strip():

        st.warning(
            "Please enter a prompt."
        )

    else:

        with st.spinner(
            "🛡️ Scanning prompt..."
        ):

            try:

                result = detect_prompt_injection(
                    prompt.strip()
                )

            except Exception as e:

                st.error(
                    f"Detection error: {e}"
                )

                st.stop()


        classification = result[
            "classification"
        ]

        risk_score = result[
            "risk_score"
        ]

        probability = result[
            "probability"
        ]


        st.divider()

        st.subheader(
            "📊 Detection Result"
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


        if classification == "SAFE":

            st.markdown(
                """
                <div class="safe-card">

                <h3>🟢 Low Risk</h3>

                <p>
                The prompt appears safe according
                to the detection model.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        elif classification == "SUSPICIOUS":

            st.markdown(
                """
                <div class="warning-card">

                <h3>🟡 Medium Risk</h3>

                <p>
                The prompt contains characteristics
                that may require additional review.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="danger-card">

                <h3>🔴 High Risk</h3>

                <p>
                The prompt is highly likely to be
                a prompt injection attempt.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )