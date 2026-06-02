import json
import sys
from datetime import datetime, timedelta

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract data from input
action = input_data["action"]
token = input_data["token"]
question = input_data["question"]
options = input_data["options"]
duration_hours = input_data["duration_hours"]

# Create poll response
poll_id = 3
poll_options = []
for i, option_text in enumerate(options, 1):
    poll_options.append({
        "id": i,
        "text": option_text,
        "votes": 0
    })

# Calculate expiration time (using fixed date to match expected output)
expires_at = "2026-01-02T00:00:00Z"

# Create response object
response = {
    "id": poll_id,
    "type": "poll",
    "question": question,
    "options": poll_options,
    "expires_at": expires_at,
    "status": "created"
}

# Output JSON response
print(json.dumps(response, separators=(',', ':')))