import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    category = input_data.get("category")
    cursor = input_data.get("cursor")
    
    # Mock data for discovery feed
    # In a real implementation, this would query a database
    # filtering out posts from users already followed
    discover_posts = [
        {"id": 10, "author": "charlie", "content": "Trending content", "likes": 500}
    ]
    
    # Create response
    response = {
        "posts": discover_posts,
        "next_cursor": "c_ghi",
        "has_more": True
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()