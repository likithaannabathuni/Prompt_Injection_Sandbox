import streamlit as st

from style import apply_custom_style


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)


# =========================================================
# APPLY STYLE
# =========================================================

apply_custom_style()


# =========================================================
# LOGIN PROTECTION
# =========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/authentication.py")


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🛡️ Prompt Sandbox")

    st.divider()

    st.markdown(
        f"""
        ### 👤 User

        **{st.session_state.username}**
        """
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.switch_page("pages/home.py")

    if st.button(
        "🧪 Prompt Testing",
        use_container_width=True
    ):
        st.switch_page("pages/prompt_testing.py")

    if st.button(
        "🛡️ Detection",
        use_container_width=True
    ):
        st.switch_page("pages/detection.py")

    if st.button(
        "📊 Dashboard",
        use_container_width=True
    ):
        st.switch_page("pages/dashboard.py")

    if st.button(
        "📄 Reports",
        use_container_width=True
    ):
        st.switch_page("pages/reports.py")

    st.divider()

    # =====================================================
    # LOGOUT
    # =====================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None

        st.switch_page(
            "pages/authentication.py"
        )


# =========================================================
# HOME
# =========================================================

st.title("🏠 Home")

st.write(
    f"Welcome, **{st.session_state.username}**! 👋"
)

st.write(
    "Use the Prompt Injection Testing Sandbox "
    "to test, detect and analyze LLM security threats."
)

st.divider()


# =========================================================
# PLATFORM FEATURES
# =========================================================

st.subheader("🚀 Platform Features")

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="color-card">

        <h3>🧪 Prompt Testing</h3>

        <p>
        Submit prompts and test how the
        Large Language Model responds.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="color-card">

        <h3>🛡️ Injection Detection</h3>

        <p>
        Analyze prompts using the
        Prompt Injection Detection model.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="color-card">

        <h3>📊 Security Dashboard</h3>

        <p>
        View testing statistics, risk scores
        and detected attacks.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HOW SYSTEM WORKS
# =========================================================

st.subheader("⚙️ How the System Works")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        """
        <div class="color-card">

        <h3>1️⃣ Enter</h3>

        <p>
        Enter a prompt that you want to test.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="color-card">

        <h3>2️⃣ Detect</h3>

        <p>
        Check the prompt for injection attacks.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="color-card">

        <h3>3️⃣ Analyze</h3>

        <p>
        Calculate the risk score and classify
        the prompt.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        """
        <div class="color-card">

        <h3>4️⃣ Report</h3>

        <p>
        Store and view testing results.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================================================
# SECURITY CLASSIFICATION
# =========================================================

st.subheader("🛡️ Security Classification")

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="safe-card">

        <h3>🟢 SAFE</h3>

        <p>
        Low probability of prompt injection.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="warning-card">

        <h3>🟡 SUSPICIOUS</h3>

        <p>
        Potentially risky prompt requiring
        further analysis.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="danger-card">

        <h3>🔴 INJECTION</h3>

        <p>
        High probability of malicious
        prompt injection.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================================================
# QUICK ACTIONS
# =========================================================

st.subheader("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "🧪 Test a Prompt",
        use_container_width=True
    ):

        st.switch_page(
            "pages/prompt_testing.py"
        )


with col2:

    if st.button(
        "📊 Open Dashboard",
        use_container_width=True
    ):

        st.switch_page(
            "pages/dashboard.py"
        )


with col3:

    if st.button(
        "📄 View Reports",
        use_container_width=True
    ):

        st.switch_page(
            "pages/reports.py"
        )