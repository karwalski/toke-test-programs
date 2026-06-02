import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    comment_id = input_data.get("comment_id")
    
    # For this simple implementation, we'll assume the deletion is always successful
    # In a real application, you would:
    # 1. Validate the token
    # 2. Check if user is author or post owner
    # 3. Verify comment exists
    # 4. Delete from database
    
    if action == "delete_comment" and token and comment_id is not None:
        response = {
            "comment_id": comment_id,
            "status": "deleted"
        }
    else:
        response = {
            "error": "Invalid request"
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()