import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract the post_id from the request
post_id = input_data["post_id"]

# Create the response
response = {
    "post_id": post_id,
    "bookmarked": False,
    "status": "removed"
}

# Output the response as JSON
print(json.dumps(response, separators=(',', ':')))