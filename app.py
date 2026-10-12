
from pathlib import Path

import pandas as pd
import streamlit as st

from src.log_parser import parse_log_file
from src.analyzer import analyze_logs


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Automated Log Analyzer",
    page_icon="📊",
    layout="wide",
)

st.title("Automated Log Analyzer")
st.caption(
    "Server log monitoring, HTTP error analysis, "
    "and rule-based anomaly detection."
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Log Source")

default_log = Path("data/sample_server.log")

uploaded_file = st.sidebar.file_uploader(
    "Upload a server log file",
    type=["log", "txt"],
)

st.sidebar.info(
    "Use logs matching the project's documented format. "
    "Uploaded files are processed for this session."
)

# -----------------------------
# Load logs
# -----------------------------
if uploaded_file is not None:
    log_text = uploaded_file.getvalue().decode(
        "utf-8", errors="replace"
    )

    records = []
    invalid_lines = []

    from src.log_parser import parse_log_line

    for line in log_text.splitlines():
        if not line.strip():
            continue

        record = parse_log_line(line)

        if record is None:
            invalid_lines.append(line)
        else:
            records.append(record)

elif default_log.exists():
    records, invalid_lines = parse_log_file(str(default_log))

else:
    st.error("No log file found. Upload a log file to continue.")
    st.stop()

# -----------------------------
# Summary metrics
# -----------------------------
result = analyze_logs(records)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Valid Requests", result["total_requests"])
col2.metric("HTTP Server Errors", result["http_errors"])
col3.metric("Server Error Rate", f'{result["error_rate"]}%')
col4.metric("Failed Login Responses", result["failed_logins"])

st.divider()

# -----------------------------
# Charts
# -----------------------------
st.subheader("Log Analytics")

if records:
    df = pd.DataFrame(records)

    left, right = st.columns(2)

    with left:
        st.markdown("**HTTP Status Code Distribution**")
        status_counts = (
            df["status_code"]
            .value_counts()
            .sort_index()
        )
        st.bar_chart(status_counts)

    with right:
        st.markdown("**Response Time by Request**")
        chart_df = df[["response_time_ms"]].reset_index(drop=True)
        chart_df.index.name = "Request"
        st.line_chart(chart_df)

    st.subheader("Parsed Log Records")

    status_filter = st.multiselect(
        "Filter by HTTP status code",
        options=sorted(df["status_code"].unique().tolist()),
        default=sorted(df["status_code"].unique().tolist()),
    )

    filtered_df = df[df["status_code"].isin(status_filter)]
    st.dataframe(filtered_df, use_container_width=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download filtered records as CSV",
        data=csv_data,
        file_name="analyzed_logs.csv",
        mime="text/csv",
    )

else:
    st.info("No valid log records were found.")

# -----------------------------
# Alerts
# -----------------------------

# -----------------------------
# Alerts
# -----------------------------
st.divider()
st.subheader("Detected Alerts")

if result["alerts"]:
    for alert in result["alerts"]:
        severity = alert["severity"]
        message = alert["message"]
        count = alert["count"]

        if severity == "CRITICAL":
            st.error(
                f"🔴 {severity}: {message} "
                f"(Count: {count})"
            )
        elif severity == "WARNING":
            st.warning(
                f"🟠 {severity}: {message} "
                f"(Count: {count})"
            )
        else:
            st.info(
                f"ℹ️ {severity}: {message} "
                f"(Count: {count})"
            )
else:
    st.success("No configured alert conditions were triggered.")


# -----------------------------
# Data quality
# -----------------------------
with st.expander("Data Quality Report"):
    st.write(f"Valid records: {len(records)}")
    st.write(f"Invalid records: {len(invalid_lines)}")

    if invalid_lines:
        st.write("Sample invalid lines:")
        st.code("\n".join(invalid_lines[:10]))
