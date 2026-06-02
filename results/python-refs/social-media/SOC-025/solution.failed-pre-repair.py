import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock database of posts
    posts_db = [
        {
            "id": 1,
            "user_id": 1,
            "content": "Hello world!",
            "created_at": "2026-01-01T00:00:00Z"
        },
        {
            "id": 2,
            "user_id": 1,
            "content": "Second post",
            "created_at": "2025-12-31T23:59:59Z"
        },
        {
            "id": 3,
            "user_id": 2,
            "content": "Other user post",
            "created_at": "2025-12-31T23:58:00Z"
        }
    ]
    
    action = input_data.get("action")
    user_id = input_data.get("user_id")
    cursor = input_data.get("cursor")
    limit = input_data.get("limit", 20)
    
    if action == "user_posts":
        # Filter posts by user_id
        user_posts = [post for post in posts_db if post["user_id"] == user_id]
        
        # Sort by created_at in reverse chronological order (newest first)
        user_posts.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Apply cursor-based pagination
        start_index = 0
        if cursor is not None:
            # Find the position after the cursor
            for i, post in enumerate(user_posts):
                if post["id"] == cursor:
                    start_index = i + 1
                    break
        
        # Get the slice of posts for this page
        page_posts = user_posts[start_index:start_index + limit]
        
        # Determine if there are more posts
        has_more = start_index + limit < len(user_posts)
        next_cursor = None
        if has_more and page_posts:
            next_cursor = page_posts[-1]["id"]
        
        # Prepare response posts (remove user_id from output)
        response_posts = []
        for post in page_posts:
            response_posts.append({
                "id": post["id"],
                "content": post["content"],
                "created_at": post["created_at"]
            })
        
        response = {
            "posts": response_posts,
            "next_cursor": next_cursor,
            "has_more": has_more
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()