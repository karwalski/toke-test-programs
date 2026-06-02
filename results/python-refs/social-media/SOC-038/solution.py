import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock database of posts
    all_posts = [
        {
            "id": 1,
            "user_id": 1,
            "text": "Just text post",
            "created_at": "2025-12-31T23:59:00Z"
        },
        {
            "id": 2,
            "user_id": 1,
            "media": [{"url": "https://img.example.com/1.jpg", "type": "image"}],
            "created_at": "2026-01-01T00:00:00Z"
        },
        {
            "id": 3,
            "user_id": 1,
            "text": "Another text post",
            "created_at": "2026-01-01T01:00:00Z"
        }
    ]
    
    # Filter posts for the requested user that contain media
    user_id = input_data["user_id"]
    media_posts = []
    
    for post in all_posts:
        if post.get("user_id") == user_id and "media" in post:
            # Create response post with only required fields
            response_post = {
                "id": post["id"],
                "media": post["media"],
                "created_at": post["created_at"]
            }
            media_posts.append(response_post)
    
    # Apply limit if specified
    limit = input_data.get("limit", len(media_posts))
    media_posts = media_posts[:limit]
    
    # Create response
    response = {
        "posts": media_posts,
        "next_cursor": None
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()