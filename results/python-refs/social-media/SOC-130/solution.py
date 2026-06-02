import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract conversation_id from the input
conversation_id = input_data["conversation_id"]

# Create the response
response = {
    "conversation_id": conversation_id,
    "all_read": True,
    "status": "marked_read"
}

# Output the response as JSON
print(json.dumps(response, separators=(',', ':')))