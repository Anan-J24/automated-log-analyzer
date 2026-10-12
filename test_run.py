from src.log_parser import parse_log_file

records, invalid_lines = parse_log_file("data/sample_server.log")

print(f"Valid records: {len(records)}")
print(f"Invalid lines: {len(invalid_lines)}")

if records:
    print("\nFirst parsed record:")
    print(records[0])

print("\nInvalid entries:")
for line in invalid_lines:
    print(line)