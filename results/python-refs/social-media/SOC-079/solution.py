import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract relevant information
action = input_data.get("action")
token = input_data.get("token")
user_id = input_data.get("user_id")

# Process the remove_follower action
if action == "remove_follower" and token and user_id is not None:
    # Simulate removing the follower (in a real app, this would interact with a database)
    response = {
        "user_id": user_id,
        "removed": True,
        "status": "follower_removed"
    }
else:
    # Handle invalid requests
    response = {
        "user_id": user_id if user_id is not None else None,
        "removed": False,
        "status": "error"
    }

# Output the response as JSON
print(json.dumps(response, separators=(',', ':')))