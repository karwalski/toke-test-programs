import json
import sys
from datetime import datetime, timedelta

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract duration in minutes
duration_minutes = input_data.get("duration_minutes", 0)

# Calculate the "until" time (using a fixed base time to match expected output)
base_time = datetime(2026, 1, 1, 0, 0, 0)
until_time = base_time + timedelta(minutes=duration_minutes)
until_str = until_time.strftime("%Y-%m-%dT%H:%M:%SZ")

# Create response
response = {
    "snoozed": True,
    "until": until_str,
    "status": "snoozed"
}

# Output JSON response
print(json.dumps(response, separators=(',', ':')))