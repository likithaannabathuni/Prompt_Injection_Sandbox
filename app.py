import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Prompt Sandbox",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None


# ============================================================
# LOGOUT FUNCTION
# ============================================================

def logout():
    """
    Clear authentication-related session data.
    """

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None

    # Clear chatbot-related session data if present
    keys_to_clear = [
        "chat_history",
        "messages",
        "uploaded_file",
        "uploaded_image",
        "current_prompt",
        "detection_result"
    ]

    for key in keys_to_clear:

        if key in st.session_state:
            del st.session_state[key]


# ============================================================
# PAGE DEFINITIONS
# ============================================================

# Home
home_page = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠"
)


# Authentication
authentication_page = st.Page(
    "pages/authentication.py",
    title="Login / Register",
    icon="🔐"
)


# AI Chatbot
chatbot_page = st.Page(
    "pages/chatbot.py",
    title="AI Chatbot",
    icon="🤖"
)


# Prompt Testing
prompt_testing_page = st.Page(
    "pages/prompt_testing.py",
    title="Prompt Testing",
    icon="🧪"
)


# Detection
detection_page = st.Page(
    "pages/detection.py",
    title="Detection",
    icon="🛡️"
)


# Dashboard
dashboard_page = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="📊"
)


# Reports
reports_page = st.Page(
    "pages/reports.py",
    title="Reports",
    icon="📄"
)


# Image Generator
image_generator_page = st.Page(
    "pages/image_generator_page.py",
    title="Image Generator",
    icon="🎨"
)


# ============================================================
# NOT LOGGED IN
# ============================================================

if not st.session_state.logged_in:

    navigation = st.navigation(
        [
            authentication_page
        ]
    )

    navigation.run()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🛡️ Prompt Sandbox"
    )

    st.caption(
        "AI Security Platform"
    )

    st.divider()


    # --------------------------------------------------------
    # USER INFORMATION
    # --------------------------------------------------------

    st.markdown(
        f"👤 **{st.session_state.username}**"
    )

    st.caption(
        "Authenticated user"
    )

    st.divider()


    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()

        st.success(
            "Logged out successfully."
        )

        st.rerun()


# ============================================================
# AUTHENTICATED NAVIGATION
# ============================================================

navigation = st.navigation(
    {
        "MAIN": [
            home_page,
            chatbot_page,
            image_generator_page
        ],

        "SECURITY": [
            prompt_testing_page,
            detection_page
        ],

        "ANALYTICS": [
            dashboard_page,
            reports_page
        ]
    }
)


# ============================================================
# RUN APPLICATION
# ============================================================

navigation.run()