import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract required fields
action = input_data.get("action")
token = input_data.get("token")
list_id = input_data.get("list_id")

# Process the subscription request
if action == "subscribe_list" and token and list_id:
    # Create response indicating successful subscription
    response = {
        "list_id": list_id,
        "subscribed": True,
        "status": "subscribed"
    }
else:
    # Handle invalid request
    response = {
        "error": "Invalid request"
    }

# Output JSON response to stdout
print(json.dumps(response, separators=(',', ':')))