import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract request components
    action = input_data.get("action")
    token = input_data.get("token")
    filters = input_data.get("filters", {})
    
    # Simulate a feed database
    all_posts = [
        {"id": 20, "content": "Low engagement post", "likes": 2, "type": "original"},
        {"id": 21, "content": "Shared content", "likes": 8, "type": "repost"},
        {"id": 22, "content": "Video content", "likes": 15, "type": "original", "media_type": "video"},
        {"id": 23, "content": "Another repost", "likes": 6, "type": "repost"},
        {"id": 24, "content": "Photo post", "likes": 3, "type": "original", "media_type": "image"},
        {"id": 25, "content": "Popular original", "likes": 10, "type": "original"}
    ]
    
    if action == "filtered_feed":
        # Apply filters
        filtered_posts = all_posts.copy()
        
        # Filter by hide_reposts
        if filters.get("hide_reposts", False):
            filtered_posts = [post for post in filtered_posts if post.get("type") != "repost"]
        
        # Filter by media_only
        if filters.get("media_only", False):
            filtered_posts = [post for post in filtered_posts if "media_type" in post]
        
        # Filter by min_likes
        min_likes = filters.get("min_likes", 0)
        if min_likes > 0:
            filtered_posts = [post for post in filtered_posts if post.get("likes", 0) >= min_likes]
        
        # Remove media_type from output to match expected format
        output_posts = []
        for post in filtered_posts:
            clean_post = {k: v for k, v in post.items() if k != "media_type"}
            output_posts.append(clean_post)
        
        # Create response
        response = {
            "posts": output_posts,
            "filters_applied": filters
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()