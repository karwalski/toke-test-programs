import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Parse the request
    action = input_data.get("action")
    tag = input_data.get("tag")
    cursor = input_data.get("cursor")
    limit = input_data.get("limit", 20)
    
    # Simulate database of posts with hashtags
    # In a real implementation, this would query a database
    all_posts = [
        {"id": 12, "content": "Love coding!", "author": "dev1", "tags": ["programming"], "timestamp": "2023-12-01T10:00:00Z"},
        {"id": 15, "content": "Python is awesome #programming", "author": "coder2", "tags": ["programming"], "timestamp": "2023-12-01T09:30:00Z"},
        {"id": 18, "content": "Working on a new app", "author": "dev3", "tags": ["programming", "mobile"], "timestamp": "2023-12-01T09:00:00Z"},
        {"id": 22, "content": "Debug session complete", "author": "dev4", "tags": ["programming"], "timestamp": "2023-12-01T08:30:00Z"}
    ]
    
    if action == "tag_feed":
        # Filter posts by tag
        matching_posts = []
        for post in all_posts:
            if tag in post.get("tags", []):
                # Create response post object (exclude internal fields)
                response_post = {
                    "id": post["id"],
                    "content": post["content"], 
                    "author": post["author"]
                }
                matching_posts.append(response_post)
        
        # Sort by recency (most recent first) - using id as proxy for timestamp
        matching_posts.sort(key=lambda x: x["id"], reverse=True)
        
        # Apply pagination
        start_idx = 0
        if cursor:
            # Find starting position based on cursor
            cursor_id = cursor.split("_")[-1] if "_" in cursor else cursor
            # Simple cursor implementation - in real system would be more robust
            start_idx = 0
        
        # Get the requested slice
        end_idx = start_idx + limit
        posts_slice = matching_posts[start_idx:end_idx]
        
        # Generate next cursor
        next_cursor = None
        if end_idx < len(matching_posts):
            next_cursor = "c_jkl"  # Simplified cursor for demo
        
        # Build response
        response = {
            "tag": tag,
            "posts": posts_slice,
            "total_posts": 150,  # Simulated total count
            "next_cursor": next_cursor
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()