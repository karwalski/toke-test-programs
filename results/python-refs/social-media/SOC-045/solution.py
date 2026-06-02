import json
import sys

def get_likes(post_id, cursor, limit):
    # Mock data - in a real system this would come from a database
    all_likes = {
        1: [
            {"id": 2, "username": "bob", "liked_at": "2026-01-01T01:00:00Z"}
        ]
    }
    
    post_likes = all_likes.get(post_id, [])
    total = len(post_likes)
    
    # Handle pagination with cursor
    start_idx = 0
    if cursor is not None:
        start_idx = cursor
    
    end_idx = start_idx + limit
    page_likes = post_likes[start_idx:end_idx]
    
    # Determine next cursor
    next_cursor = None
    if end_idx < total:
        next_cursor = end_idx
    
    return {
        "post_id": post_id,
        "likers": page_likes,
        "total": total,
        "next_cursor": next_cursor
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract parameters
action = input_data["action"]
post_id = input_data["post_id"]
cursor = input_data["cursor"]
limit = input_data["limit"]

# Process request
if action == "get_likes":
    result = get_likes(post_id, cursor, limit)
    print(json.dumps(result, separators=(',', ':')))