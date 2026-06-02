import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    
    # Simple validation
    if action != "unlike_post" or not token or post_id is None:
        response = {"error": "Invalid request"}
    else:
        # Simulate removing a like (in a real system, this would interact with a database)
        # For this example, we'll assume the unlike operation is successful
        response = {
            "post_id": post_id,
            "liked": False,
            "like_count": 0,
            "status": "unliked"
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()