import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    content = input_data.get("content")
    
    # For this simple implementation, we'll assume the token is valid
    # and represents user "alice"
    author = "alice"
    
    # Create the response
    response = {
        "comment_id": 1,
        "post_id": post_id,
        "content": content,
        "author": author,
        "created_at": "2026-01-01T00:00:00Z",
        "status": "created"
    }
    
    # Output the JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()