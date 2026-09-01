import streamlit as st
import pandas as pd
from io import BytesIO

from style import apply_custom_style
from database import get_connection

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


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

st.title("📄 Security Reports")

st.write(
    "Generate and download reports of your "
    "prompt injection testing activity."
)


# ==========================================
# DATABASE
# ==========================================

conn = get_connection()

query = """
SELECT
    id,
    prompt_text,
    llm_response,
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

        <h2>📄 No Reports Yet</h2>

        <p>
        Perform some prompt injection tests
        to generate your first report.
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
# SUMMARY
# ==========================================

st.subheader("📊 Report Summary")


col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric("Total Tests", total_tests)

with col2:
    st.metric("🟢 Safe", safe_count)

with col3:
    st.metric("🟡 Suspicious", suspicious_count)

with col4:
    st.metric("🔴 Injection", injection_count)

with col5:
    st.metric(
        "Average Risk",
        f"{average_risk:.2f}"
    )


st.divider()


# ==========================================
# TABLE
# ==========================================

st.subheader("📋 Testing Results")


display_df = df[
    [
        "id",
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
        "id": "ID",
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


st.divider()


# ==========================================
# CSV
# ==========================================

st.subheader("📥 Download CSV")


csv_data = df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    "📥 Download CSV Report",
    data=csv_data,
    file_name="prompt_injection_report.csv",
    mime="text/csv",
    use_container_width=True
)


# ==========================================
# PDF
# ==========================================

def create_pdf():

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Prompt Injection Security Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    elements.append(
        Paragraph(
            f"User: {st.session_state.username}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    summary_data = [
        ["Metric", "Value"],
        ["Total Tests", str(total_tests)],
        ["Safe", str(safe_count)],
        ["Suspicious", str(suspicious_count)],
        ["Injection", str(injection_count)],
        [
            "Average Risk Score",
            f"{average_risk:.2f}"
        ]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[250, 150]
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#6a11cb")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER"
                )
            ]
        )
    )

    elements.append(
        summary_table
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "Testing Results",
            styles["Heading2"]
        )
    )

    table_data = [
        [
            "ID",
            "Classification",
            "Risk",
            "Date"
        ]
    ]

    for _, row in df.iterrows():

        table_data.append(
            [
                str(row["id"]),
                str(row["detection_result"]),
                f"{row['risk_score']:.2f}",
                str(row["created_at"])
            ]
        )

    results_table = Table(
        table_data,
        colWidths=[
            40,
            150,
            70,
            180
        ]
    )

    results_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#2575fc")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )

    elements.append(
        results_table
    )

    document.build(elements)

    buffer.seek(0)

    return buffer.getvalue()


# ==========================================
# PDF DOWNLOAD
# ==========================================

st.subheader("📄 Download PDF")


try:

    pdf_data = create_pdf()

    st.download_button(
        "📄 Download PDF Report",
        data=pdf_data,
        file_name="prompt_injection_security_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

except Exception as e:

    st.error(
        f"Could not generate PDF: {e}"
    )