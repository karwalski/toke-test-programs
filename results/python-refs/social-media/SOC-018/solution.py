import json
import sys

# Mock database of posts
posts_db = {
    1: {
        "id": 1,
        "author": {"id": 1, "username": "alice"},
        "content": "Hello world!",
        "likes": 0,
        "shares": 0,
        "comments": 0,
        "created_at": "2026-01-01T00:00:00Z"
    }
}

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract post_id from the request
post_id = input_data["post_id"]

# Retrieve the post from mock database
if post_id in posts_db:
    response = posts_db[post_id]
else:
    response = {"error": "Post not found"}

# Output response as JSON
print(json.dumps(response, separators=(',', ':')))