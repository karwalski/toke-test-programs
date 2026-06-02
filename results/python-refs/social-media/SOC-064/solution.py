import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract the comment_id from the input
comment_id = input_data["comment_id"]

# Create the response
response = {
    "comment_id": comment_id,
    "liked": True,
    "like_count": 1,
    "status": "liked"
}

# Output the response as JSON
print(json.dumps(response, separators=(',', ':')))