import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract the user_id from the request
user_id = input_data["user_id"]

# Create the response
response = {
    "user_id": user_id,
    "following": False,
    "status": "unfollowed"
}

# Output the JSON response
print(json.dumps(response, separators=(',', ':')))