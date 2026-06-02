import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract data from input
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    
    # Simple validation
    if action != "like_post" or not token or post_id is None:
        response = {"error": "Invalid request"}
    else:
        # For this simple implementation, we'll assume the like operation succeeds
        # In a real system, you would validate the token and check the database
        response = {
            "post_id": post_id,
            "liked": True,
            "like_count": 1,
            "status": "liked"
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()