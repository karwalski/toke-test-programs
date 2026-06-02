import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract required fields
action = input_data.get("action")
token = input_data.get("token")
message_id = input_data.get("message_id")
emoji = input_data.get("emoji")

# For this simple implementation, we'll assume the reaction is always successful
# and this is the first reaction of this type to the message
response = {
    "message_id": message_id,
    "emoji": emoji,
    "reactions": {emoji: 1},
    "status": "reacted"
}

# Output the response as JSON
print(json.dumps(response, separators=(',', ':')))