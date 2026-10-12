
from src.log_parser import parse_log_file
from src.analyzer import analyze_logs


def test_analyzer_with_sample_logs():
    records, _ = parse_log_file("data/sample_server.log")
    result = analyze_logs(records)

    assert result["total_requests"] == 10
    assert result["http_errors"] == 3
    assert result["failed_logins"] == 3
    assert result["slow_requests"] == 3
    assert result["error_rate"] == 30.0


def test_analyzer_with_empty_logs():
    result = analyze_logs([])

    assert result["total_requests"] == 0
    assert result["http_errors"] == 0
    assert result["alerts"] == []
