import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract required fields
post_id = input_data["post_id"]
reason = input_data["reason"]

# Create response
response = {
    "report_id": "rpt_001",
    "post_id": post_id,
    "reason": reason,
    "status": "submitted"
}

# Output JSON response
print(json.dumps(response, separators=(',', ':')))