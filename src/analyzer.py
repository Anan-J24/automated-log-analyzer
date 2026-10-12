
import pandas as pd


def analyze_logs(
    records: list[dict],
    slow_request_threshold: int = 100,
    failed_login_threshold: int = 3,
) -> dict:
    """Analyze log records and generate structured alerts."""

    columns = [
        "timestamp",
        "level",
        "method",
        "path",
        "status_code",
        "response_time_ms",
    ]

    df = pd.DataFrame(records, columns=columns)

    if df.empty:
        return {
            "total_requests": 0,
            "http_errors": 0,
            "error_rate": 0.0,
            "failed_logins": 0,
            "slow_requests": 0,
            "alerts": [],
            "status_counts": {},
        }

    # Ensure numeric columns contain valid numbers.
    df["status_code"] = pd.to_numeric(
        df["status_code"], errors="coerce"
    )
    df["response_time_ms"] = pd.to_numeric(
        df["response_time_ms"], errors="coerce"
    )

    total_requests = len(df)

    http_errors = int(
        (df["status_code"] >= 500).sum()
    )

    error_rate = round(
        (http_errors / total_requests) * 100, 2
    )

    failed_logins = int(
        (
            (df["path"] == "/login")
            & (df["method"] == "POST")
            & (df["status_code"] == 401)
        ).sum()
    )

    slow_requests = int(
        (
            df["response_time_ms"]
            > slow_request_threshold
        ).sum()
    )

    alerts = []

    # Critical: server-side HTTP errors.
    if http_errors > 0:
        alerts.append({
            "severity": "CRITICAL",
            "type": "server_errors",
            "message": (
                f"{http_errors} server error(s) detected."
            ),
            "count": http_errors,
        })

    # Warning: repeated failed login responses.
    if failed_logins >= failed_login_threshold:
        alerts.append({
            "severity": "WARNING",
            "type": "failed_logins",
            "message": (
                f"{failed_logins} failed login response(s) "
                "detected."
            ),
            "count": failed_logins,
        })

    # Warning: requests exceeding the configured threshold.
    if slow_requests > 0:
        alerts.append({
            "severity": "WARNING",
            "type": "slow_requests",
            "message": (
                f"{slow_requests} slow request(s) detected "
                f"(over {slow_request_threshold} ms)."
            ),
            "count": slow_requests,
        })

    valid_status_codes = df["status_code"].dropna()

    status_counts = {
        int(code): int(count)
        for code, count in valid_status_codes
        .value_counts()
        .items()
    }

    return {
        "total_requests": total_requests,
        "http_errors": http_errors,
        "error_rate": error_rate,
        "failed_logins": failed_logins,
        "slow_requests": slow_requests,
        "alerts": alerts,
        "status_counts": status_counts,
    }
