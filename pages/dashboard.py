import streamlit as st
import pandas as pd

from style import apply_custom_style
from database import get_connection


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

st.title("📊 Security Dashboard")

st.write(
    "Monitor prompt injection testing activity "
    "and security results."
)


# ==========================================
# GET DATA
# ==========================================

conn = get_connection()

query = """
SELECT
    id,
    prompt_text,
    detection_result,
    risk_score,
    model,
    created_at
FROM test_results
WHERE user_id = ?
ORDER BY created_at DESC
"""

df = pd.read_sql_query(
    query,
    conn,
    params=(
        st.session_state.user_id,
    )
)

conn.close()


if df.empty:

    st.markdown(
        """
        <div class="gradient-card">

        <h2>📊 Your Dashboard Is Ready!</h2>

        <p>
        Perform some prompt tests to start
        generating security analytics.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🧪 Start Testing",
        use_container_width=True
    ):

        st.switch_page(
            "pages/prompt_testing.py"
        )

    st.stop()


# ==========================================
# STATISTICS
# ==========================================

total_tests = len(df)

safe_count = len(
    df[df["detection_result"] == "SAFE"]
)

suspicious_count = len(
    df[df["detection_result"] == "SUSPICIOUS"]
)

injection_count = len(
    df[df["detection_result"] == "INJECTION"]
)

average_risk = df["risk_score"].mean()


# ==========================================
# METRICS
# ==========================================

st.subheader("📈 Security Overview")


col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric("🧪 Total Tests", total_tests)

with col2:
    st.metric("🟢 Safe", safe_count)

with col3:
    st.metric("🟡 Suspicious", suspicious_count)

with col4:
    st.metric("🔴 Injection", injection_count)

with col5:
    st.metric(
        "⚠️ Avg Risk",
        f"{average_risk:.2f}"
    )


st.divider()


# ==========================================
# SECURITY STATUS
# ==========================================

st.subheader("🛡️ Current Security Status")


if injection_count > 0:

    st.markdown(
        f"""
        <div class="danger-card">

        <h3>🚨 Security Alert</h3>

        <p>
        {injection_count} prompt injection attack(s)
        have been detected.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

elif suspicious_count > 0:

    st.markdown(
        f"""
        <div class="warning-card">

        <h3>⚠️ Attention Required</h3>

        <p>
        {suspicious_count} suspicious prompt(s)
        have been detected.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="safe-card">

        <h3>✅ System Looks Safe</h3>

        <p>
        No prompt injection attacks have
        been detected.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# CLASSIFICATION CHART
# ==========================================

st.subheader("📊 Prompt Classification")


classification_data = pd.DataFrame(
    {
        "Classification": [
            "Safe",
            "Suspicious",
            "Injection"
        ],
        "Count": [
            safe_count,
            suspicious_count,
            injection_count
        ]
    }
)


st.bar_chart(
    classification_data.set_index(
        "Classification"
    )
)


# ==========================================
# RISK CHART
# ==========================================

st.subheader("📈 Risk Score History")


risk_chart = df[
    ["created_at", "risk_score"]
].copy()

risk_chart["created_at"] = pd.to_datetime(
    risk_chart["created_at"]
)

risk_chart = risk_chart.sort_values(
    "created_at"
)

risk_chart = risk_chart.set_index(
    "created_at"
)


st.line_chart(
    risk_chart["risk_score"]
)


# ==========================================
# HISTORY
# ==========================================

st.subheader("📋 Recent Testing History")


display_df = df[
    [
        "prompt_text",
        "detection_result",
        "risk_score",
        "model",
        "created_at"
    ]
].copy()


display_df["risk_score"] = display_df[
    "risk_score"
].round(2)


display_df = display_df.rename(
    columns={
        "prompt_text": "Prompt",
        "detection_result": "Classification",
        "risk_score": "Risk Score",
        "model": "LLM Model",
        "created_at": "Date"
    }
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)