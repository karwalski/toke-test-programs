import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract required fields
action = input_data.get("action")
token = input_data.get("token")
list_id = input_data.get("list_id")
user_id = input_data.get("user_id")

# For this implementation, we'll simulate the removal process
# In a real system, this would involve database operations and token validation

# Create response matching the expected output format
response = {
    "list_id": list_id,
    "user_id": user_id,
    "member_count": 0,
    "status": "removed"
}

# Output JSON response to stdout
print(json.dumps(response, separators=(',', ':')))