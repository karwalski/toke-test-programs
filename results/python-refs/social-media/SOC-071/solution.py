import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract user_id from the input
    user_id = input_data["user_id"]
    
    # Create the response
    response = {
        "user_id": user_id,
        "following": True,
        "status": "followed"
    }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()