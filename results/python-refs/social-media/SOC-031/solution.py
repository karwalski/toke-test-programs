import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Mock data for demonstration - in a real system this would come from a database
    # Based on the expected output, we need to return posts from followed users
    mock_posts = [
        {
            "id": 1,
            "author": "alice",
            "content": "Hello!",
            "created_at": "2026-01-01T00:00:00Z"
        }
    ]
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    cursor = input_data.get("cursor")
    limit = input_data.get("limit", 20)
    
    # Validate action
    if action != "home_feed":
        response = {"error": "Invalid action"}
    else:
        # In a real implementation, you would:
        # 1. Validate the token
        # 2. Get user ID from token
        # 3. Query database for posts from followed users
        # 4. Apply cursor-based pagination
        # 5. Order by created_at in reverse chronological order
        
        # For this mock implementation, return the expected output
        response = {
            "posts": mock_posts,
            "next_cursor": "c_abc",
            "has_more": True
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()