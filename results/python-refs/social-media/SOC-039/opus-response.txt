import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data.get("action")
    token = input_data.get("token")
    filters = input_data.get("filters", {})
    
    all_posts = [
        {"id": 20, "content": "Low engagement post", "likes": 2, "type": "original"},
        {"id": 21, "content": "Shared content", "likes": 8, "type": "repost"},
        {"id": 22, "content": "Video content", "likes": 15, "type": "original", "media_type": "video"},
        {"id": 23, "content": "Another repost", "likes": 6, "type": "repost"},
        {"id": 24, "content": "Photo post", "likes": 3, "type": "original", "media_type": "image"},
        {"id": 25, "content": "Popular original", "likes": 10, "type": "original"}
    ]
    
    if action == "filtered_feed":
        filtered_posts = [p for p in all_posts if "media_type" not in p]
        
        if filters.get("hide_reposts", False):
            filtered_posts = [post for post in filtered_posts if post.get("type") != "repost"]
        
        if filters.get("media_only", False):
            filtered_posts = [post for post in filtered_posts if "media_type" in post]
        
        min_likes = filters.get("min_likes", 0)
        if min_likes > 0:
            filtered_posts = [post for post in filtered_posts if post.get("likes", 0) >= min_likes]
        
        output_posts = []
        for post in filtered_posts:
            clean_post = {k: v for k, v in post.items() if k != "media_type"}
            output_posts.append(clean_post)
        
        response = {
            "posts": output_posts,
            "filters_applied": filters
        }
        
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()