import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    posts_db = [
        {"id": 1, "user_id": 1, "content": "Hello world!", "created_at": "2026-01-01T00:00:00Z"},
    ]
    
    action = input_data.get("action")
    user_id = input_data.get("user_id")
    cursor = input_data.get("cursor")
    limit = input_data.get("limit", 20)
    
    if action == "user_posts":
        user_posts = [post for post in posts_db if post["user_id"] == user_id]
        user_posts.sort(key=lambda x: x["created_at"], reverse=True)
        
        start_index = 0
        if cursor is not None:
            for i, post in enumerate(user_posts):
                if post["id"] == cursor:
                    start_index = i + 1
                    break
        
        page_posts = user_posts[start_index:start_index + limit]
        has_more = start_index + limit < len(user_posts)
        next_cursor = None
        if has_more and page_posts:
            next_cursor = page_posts[-1]["id"]
        
        response_posts = [{"id": p["id"], "content": p["content"], "created_at": p["created_at"]} for p in page_posts]
        
        response = {
            "posts": response_posts,
            "next_cursor": next_cursor,
            "has_more": has_more
        }
        
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()