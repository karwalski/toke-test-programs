import json
import sys
from datetime import datetime

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract data from input
action = input_data.get("action")
token = input_data.get("token")
user_id = input_data.get("user_id")

# Simulate sending follow request (in real app, this would validate token and make API call)
if action == "follow_request" and token and user_id:
    response = {
        "user_id": user_id,
        "status": "pending",
        "requested_at": "2026-01-01T00:00:00Z"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))