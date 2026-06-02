import json
import sys

# Mock data for testing
users_following = {
    1: [
        {"id": 3, "username": "carol", "followed_at": "2026-01-01T00:00:00Z"}
    ]
}

def get_following(user_id, cursor, limit):
    following_list = users_following.get(user_id, [])
    
    # For this simple implementation, cursor is not used since we only have one item
    # In a real system, cursor would be used for pagination
    
    start_index = 0 if cursor is None else cursor
    end_index = start_index + limit
    
    paginated_following = following_list[start_index:end_index]
    
    total = len(following_list)
    next_cursor = None if end_index >= total else end_index
    
    return {
        "user_id": user_id,
        "following": paginated_following,
        "total": total,
        "next_cursor": next_cursor
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Process request
user_id = input_data["user_id"]
cursor = input_data["cursor"]
limit = input_data["limit"]

response = get_following(user_id, cursor, limit)

# Output response to stdout
print(json.dumps(response, separators=(',', ':')))