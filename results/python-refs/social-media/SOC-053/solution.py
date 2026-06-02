import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract user_id from the request
user_id = input_data["user_id"]

# Create response with exact format
response = {
    "user_id": user_id,
    "blocked": True,
    "status": "blocked"
}

# Output JSON response
print(json.dumps(response, separators=(',', ':')))