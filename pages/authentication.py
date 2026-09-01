import sqlite3
import hashlib
import streamlit as st

from style import apply_custom_style


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Prompt Sandbox - Authentication",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

apply_custom_style()


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "users.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


create_database()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# REGISTER USER
# ============================================================

def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ============================================================
# LOGIN USER
# ============================================================

def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


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
# IF USER IS ALREADY LOGGED IN
# ============================================================

if st.session_state.logged_in:

    st.title("🛡️ Prompt Sandbox")

    st.success(
        f"Welcome back, {st.session_state.username}!"
    )

    if st.button(
        "🏠 Go to Home",
        type="primary",
        use_container_width=True
    ):

        st.switch_page("pages/home.py")

    st.stop()


# ============================================================
# TOP SPACING
# ============================================================

st.write("")
st.write("")


# ============================================================
# APPLICATION BRANDING
# ============================================================

st.title("🛡️ Prompt Sandbox")

st.caption(
    "Secure AI Testing & LLM Protection Platform"
)

st.write("")


# ============================================================
# AUTHENTICATION TABS
# ============================================================

login_tab, register_tab = st.tabs(
    [
        "🔐 Login",
        "✨ Create Account"
    ]
)


# ============================================================
# LOGIN TAB
# ============================================================

with login_tab:

    st.subheader("Welcome back")

    st.caption(
        "Sign in to continue to your workspace."
    )

    st.write("")

    username = st.text_input(
        "Username",
        placeholder="Enter your username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="login_password"
    )

    st.write("")

    login_button = st.button(
        "Sign In",
        type="primary",
        use_container_width=True
    )

    if login_button:

        username = username.strip()

        if username == "":

            st.warning(
                "Please enter your username."
            )

        elif password == "":

            st.warning(
                "Please enter your password."
            )

        else:

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]

                st.success(
                    "Login successful!"
                )

                st.switch_page(
                    "pages/home.py"
                )

            else:

                st.error(
                    "Invalid username or password."
                )


# ============================================================
# REGISTER TAB
# ============================================================

with register_tab:

    st.subheader("Create your account")

    st.caption(
        "Create an account to access the AI security platform."
    )

    st.write("")

    new_username = st.text_input(
        "Username",
        placeholder="Choose a username",
        key="register_username"
    )

    new_password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter your password",
        key="register_confirm_password"
    )

    st.write("")

    register_button = st.button(
        "Create Account",
        type="primary",
        use_container_width=True
    )

    if register_button:

        new_username = new_username.strip()

        if new_username == "":

            st.warning(
                "Please enter a username."
            )

        elif len(new_username) < 3:

            st.warning(
                "Username must contain at least 3 characters."
            )

        elif new_password == "":

            st.warning(
                "Please create a password."
            )

        elif len(new_password) < 6:

            st.warning(
                "Password must contain at least 6 characters."
            )

        elif new_password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        else:

            created = register_user(
                new_username,
                new_password
            )

            if created:

                st.success(
                    "Account created successfully!"
                )

                st.info(
                    "Go to the Login tab and sign in."
                )

            else:

                st.error(
                    "This username already exists."
                )


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.write("")

st.divider()

st.caption(
    "🔒 Secure authentication"
)

st.caption(
    "Prompt Sandbox • AI Security Platform"
)