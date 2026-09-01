import streamlit as st


def apply_custom_style():
    """
    Common professional UI theme for the entire application.
    """

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        .stApp {
            background: #f5f7fb;
        }

        .block-container {
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {
            background: #111827;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff;
        }

        section[data-testid="stSidebar"] .stButton button {
            background: transparent;
            color: #e5e7eb;
            border: none;
            border-radius: 10px;
            text-align: left;
            font-size: 14px;
            font-weight: 600;
            min-height: 42px;
            transition: 0.2s;
        }

        section[data-testid="stSidebar"]
        .stButton button:hover {
            background: #1f2937;
            color: #ffffff;
        }


        /* =====================================================
           HEADINGS
        ===================================================== */

        h1 {
            color: #111827 !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        h2 {
            color: #111827 !important;
            font-weight: 750 !important;
        }

        h3 {
            color: #1f2937 !important;
            font-weight: 700 !important;
        }


        /* =====================================================
           TEXT
        ===================================================== */

        p {
            color: #4b5563;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {
            border-radius: 10px;
            border: 1px solid #d1d5db;
            background: #ffffff;
            color: #111827;
            font-weight: 600;
            min-height: 42px;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            border-color: #4f46e5;
            color: #4f46e5;
            background: #f5f3ff;
        }


        /* =====================================================
           PRIMARY BUTTON
        ===================================================== */

        .stButton > button[kind="primary"] {
            background: #4f46e5;
            color: white;
            border: none;
        }

        .stButton > button[kind="primary"]:hover {
            background: #4338ca;
            color: white;
        }


        /* =====================================================
           INPUTS
        ===================================================== */

        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"],
        .stNumberInput input {
            border-radius: 10px !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: #4f46e5 !important;
            box-shadow: 0 0 0 1px #4f46e5 !important;
        }


        /* =====================================================
           FILE UPLOADER
        ===================================================== */

        section[data-testid="stFileUploaderDropzone"] {
            background: #ffffff;
            border: 2px dashed #c7d2fe;
            border-radius: 14px;
        }


        /* =====================================================
           EXPANDERS
        ===================================================== */

        div[data-testid="stExpander"] {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
        }


        /* =====================================================
           CHAT
        ===================================================== */

        div[data-testid="stChatMessage"] {
            border-radius: 12px;
            margin-bottom: 10px;
        }

        div[data-testid="stChatInput"] {
            border-radius: 12px;
        }


        /* =====================================================
           ALERTS
        ===================================================== */

        div[data-testid="stAlert"] {
            border-radius: 10px;
        }


        /* =====================================================
           METRICS
        ===================================================== */

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 16px;
        }


        /* =====================================================
           TABLE
        ===================================================== */

        div[data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
        }


        /* =====================================================
           DIVIDER
        ===================================================== */

        hr {
            border-color: #e5e7eb;
        }


        /* =====================================================
           LOGIN CARD
        ===================================================== */

        .login-container {
            max-width: 460px;
            margin: 40px auto 0 auto;
        }

        .login-brand {
            text-align: center;
            margin-bottom: 30px;
        }

        .login-logo {
            width: 70px;
            height: 70px;
            margin: auto;
            border-radius: 18px;
            background: #4f46e5;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.20);
        }

        .login-title {
            font-size: 30px;
            font-weight: 800;
            color: #111827;
            margin-top: 18px;
        }

        .login-subtitle {
            color: #6b7280;
            font-size: 14px;
            margin-top: 5px;
        }


        /* =====================================================
           FEATURE CARDS
        ===================================================== */

        .feature-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 22px;
            min-height: 150px;
            transition: 0.2s;
        }

        .feature-card:hover {
            border-color: #c7d2fe;
            box-shadow: 0 8px 25px rgba(17, 24, 39, 0.06);
        }

        .feature-icon {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .feature-title {
            font-size: 17px;
            font-weight: 700;
            color: #111827;
        }

        .feature-text {
            font-size: 13px;
            color: #6b7280;
            margin-top: 5px;
        }


        /* =====================================================
           STATUS CARD
        ===================================================== */

        .status-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 20px;
        }


        /* =====================================================
           MOBILE
        ===================================================== */

        @media (max-width: 768px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .login-container {
                margin-top: 20px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )