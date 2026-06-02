import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract relevant information
action = input_data.get("action")
token = input_data.get("token")
user_id = input_data.get("user_id")
duration = input_data.get("duration")

# Process mute request
if action == "mute_user":
    # Create response
    response = {
        "user_id": user_id,
        "muted": True,
        "duration": duration,
        "status": "muted"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))