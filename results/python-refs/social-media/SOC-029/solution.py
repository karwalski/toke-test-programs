import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract fields from input
action = input_data.get("action")
token = input_data.get("token")
post_id = input_data.get("post_id")
warning_text = input_data.get("warning_text")

# Process the action
if action == "add_content_warning":
    response = {
        "post_id": post_id,
        "content_warning": warning_text,
        "status": "updated"
    }
elif action == "remove_content_warning":
    response = {
        "post_id": post_id,
        "content_warning": None,
        "status": "updated"
    }
else:
    response = {
        "post_id": post_id,
        "status": "error"
    }

# Output JSON response
print(json.dumps(response, separators=(',', ':')))