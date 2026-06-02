import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    request = json.loads(input_data)
    
    # Extract post_id from request
    post_id = request.get("post_id")
    
    # Create response
    response = {
        "post_id": post_id,
        "bookmarked": True,
        "status": "bookmarked"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()