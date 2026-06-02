import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Extract required fields
action = input_data["action"]
token = input_data["token"]
comment_id = input_data["comment_id"]
reason = input_data["reason"]

# Create response
response = {
    "report_id": "rpt_002",
    "comment_id": comment_id,
    "reason": reason,
    "status": "submitted"
}

# Output JSON response
print(json.dumps(response, separators=(',', ':')))