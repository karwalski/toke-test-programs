import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract user_id from the request
user_id = input_data["user_id"]

# Create the response
response = {
    "user_id": user_id,
    "blocked": False,
    "status": "unblocked"
}

# Output the response as JSON
print(json.dumps(response, separators=(',', ':')))