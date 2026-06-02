import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse the JSON input
endpoint_specs = json.loads(input_data)

# Generate monitoring configuration
monitoring_config = {
    "monitors": []
}

# Process each endpoint spec
for spec in endpoint_specs:
    monitor = {
        "check_interval_sec": spec["check_interval_sec"],
        "expected_status": spec["expected_status"],
        "method": spec["method"],
        "name": spec["name"],
        "url": spec["url"]
    }
    monitoring_config["monitors"].append(monitor)

# Output JSON to stdout with no spaces after separators to match expected format
print(json.dumps(monitoring_config, separators=(',', ':')))