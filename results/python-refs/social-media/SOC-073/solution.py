import json
import sys

def get_followers(user_id, cursor, limit):
    # Mock data - in a real system this would come from a database
    all_followers = {
        1: [
            {"id": 2, "username": "bob", "followed_at": "2026-01-01T00:00:00Z"}
        ]
    }
    
    followers = all_followers.get(user_id, [])
    total = len(followers)
    
    # Handle pagination
    start_index = 0
    if cursor is not None:
        start_index = cursor
    
    # Get the requested page
    end_index = start_index + limit
    page_followers = followers[start_index:end_index]
    
    # Determine next cursor
    next_cursor = None
    if end_index < total:
        next_cursor = end_index
    
    return {
        "user_id": user_id,
        "followers": page_followers,
        "total": total,
        "next_cursor": next_cursor
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process the request
if input_data["action"] == "get_followers":
    result = get_followers(
        input_data["user_id"],
        input_data["cursor"],
        input_data["limit"]
    )
    
    # Output JSON response
    print(json.dumps(result, separators=(',', ':')))