import json
import sys

def get_comments(post_id, sort, cursor, limit):
    # Mock data - in a real app this would come from a database
    all_comments = {
        1: [
            {"id": 1, "content": "Great post!", "author": "alice", "likes": 0, "replies": 1, "timestamp": 1}
        ]
    }
    
    # Get comments for the post
    comments = all_comments.get(post_id, [])
    
    # Sort comments
    if sort == "recent":
        comments.sort(key=lambda x: x["timestamp"], reverse=True)
    elif sort == "popularity":
        comments.sort(key=lambda x: x["likes"], reverse=True)
    
    # Handle pagination
    start_idx = 0
    if cursor is not None:
        start_idx = cursor
    
    end_idx = start_idx + limit
    paginated_comments = comments[start_idx:end_idx]
    
    # Calculate next cursor
    next_cursor = None
    if end_idx < len(comments):
        next_cursor = end_idx
    
    # Remove timestamp from output (it was only used for sorting)
    for comment in paginated_comments:
        comment.pop("timestamp", None)
    
    return {
        "post_id": post_id,
        "comments": paginated_comments,
        "total": len(paginated_comments),
        "next_cursor": next_cursor
    }

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract parameters
action = input_data["action"]
post_id = input_data["post_id"]
sort = input_data["sort"]
cursor = input_data["cursor"]
limit = input_data["limit"]

# Process request
if action == "get_comments":
    result = get_comments(post_id, sort, cursor, limit)
    print(json.dumps(result, separators=(',', ':')))