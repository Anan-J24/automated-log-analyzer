
from src.log_parser import parse_log_line


def test_valid_log_line():
    line = "2026-10-12 10:00:03 ERROR GET /api/orders 500 120ms"

    result = parse_log_line(line)

    assert result is not None
    assert result["level"] == "ERROR"
    assert result["method"] == "GET"
    assert result["path"] == "/api/orders"
    assert result["status_code"] == 500
    assert result["response_time_ms"] == 120


def test_invalid_log_line():
    result = parse_log_line("invalid log entry")

    assert result is None


def test_invalid_timestamp():
    line = "2026-99-99 10:00:03 ERROR GET /api/orders 500 120ms"

    result = parse_log_line(line)

    assert result is None

