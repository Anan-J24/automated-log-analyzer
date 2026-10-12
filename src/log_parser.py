
import re
from datetime import datetime
from pathlib import Path


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} "
    r"\d{2}:\d{2}:\d{2}) "
    r"(?P<level>INFO|WARNING|ERROR) "
    r"(?P<method>GET|POST|PUT|DELETE|PATCH) "
    r"(?P<path>/\S*) "
    r"(?P<status_code>\d{3}) "
    r"(?P<response_time_ms>\d+)ms$"
)


def parse_log_line(line: str) -> dict | None:
    match = LOG_PATTERN.fullmatch(line.strip())

    if not match:
        return None

    data = match.groupdict()

    try:
        timestamp = datetime.strptime(
            data["timestamp"], "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return None

    return {
        "timestamp": timestamp,
        "level": data["level"],
        "method": data["method"],
        "path": data["path"],
        "status_code": int(data["status_code"]),
        "response_time_ms": int(data["response_time_ms"]),
    }


def parse_log_file(file_path: str) -> tuple[list[dict], list[str]]:
    records = []
    invalid_lines = []

    with Path(file_path).open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = parse_log_line(line)

            if record is None:
                invalid_lines.append(line.rstrip("\n"))
            else:
                records.append(record)

    return records, invalid_lines
