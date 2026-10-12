# Automated Log Analyzer & IT Alerting System

A Python-based log analysis application that parses server logs, calculates HTTP error metrics, detects configured alert conditions, and presents results through an interactive Streamlit dashboard.

## Features

- **Log parsing:** Extract timestamps, log levels, HTTP methods, endpoints, status codes, and response times.
- **Error analytics:** Calculate total requests, server errors, and server error rate.
- **Rule-based alerts:** Identify server-side HTTP errors, repeated failed login responses, and slow requests.
- **Interactive dashboard:** Visualize HTTP status codes and response times.
- **Log filtering:** Filter records by HTTP status code.
- **CSV export:** Download filtered log records for further analysis.
- **Data quality reporting:** Count valid and invalid log entries.
- **Automated tests:** Test log parsing, invalid input handling, and analysis behavior.

## Technology Stack

- Python
- Pandas
- Streamlit
- Pytest

## Project Structure

```text
automated-log-analyzer/
├── app.py
├── src/
│   ├── analyzer.py
│   └── log_parser.py
├── data/
│   └── sample_server.log
├── tests/
│   ├── test_analyzer.py
│   └── test_parser.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd automated-log-analyzer
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the dashboard

```powershell
python -m streamlit run app.py
```

### 5. Run the tests

```powershell
python -m pytest tests -v
```

## Alert Rules

| Condition | Severity |
|---|---|
| HTTP server-side errors (status codes 500 and above) | CRITICAL |
| Failed login responses reach the configured threshold | WARNING |
| Response time exceeds the configured threshold | WARNING |

These are rule-based alerts for analysis and demonstration. They do not independently confirm a security incident or service outage.

## Sample Data

The repository includes synthetic server log entries for demonstrating parsing, analytics, alert rules, and invalid-line handling. Use logs you are authorized to analyze.

## Future Improvements

- Persistent storage with SQLite
- Configurable alert thresholds through the dashboard
- Alert history and reporting
- Additional log formats
- Optional email notifications
- Deployment and containerization

## Project Status

This project is under active development. Features and tests are being improved incrementally.

## Author

Developed as a Python portfolio project focused on log analysis, monitoring concepts, and data visualization.