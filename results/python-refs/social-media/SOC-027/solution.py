import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    quote = input_data.get("quote")
    
    # Create response object
    response = {
        "id": 8,
        "type": "repost",
        "original_post_id": post_id,
        "quote": quote,
        "status": "created"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()