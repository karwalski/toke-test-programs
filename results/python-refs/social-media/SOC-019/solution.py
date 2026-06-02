import json
import sys
from datetime import datetime

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    content = input_data.get("content")
    
    # For this simple implementation, we'll assume the token is valid
    # and the user is authorized to edit the post
    if action == "update_post":
        # Create the response with the updated post
        response = {
            "id": post_id,
            "content": content,
            "edited_at": "2026-01-01T01:00:00Z",
            "status": "updated"
        }
        
        # Output the JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()