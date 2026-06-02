import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    comment_id = input_data.get("comment_id")
    
    # For this implementation, we'll assume the pin operation is successful
    # In a real system, you would validate the token, check permissions, etc.
    
    if action == "pin_comment":
        response = {
            "comment_id": comment_id,
            "pinned": True,
            "status": "pinned"
        }
    else:
        response = {
            "error": "Invalid action"
        }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()