import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract the required fields
    action = input_data.get("action")
    token = input_data.get("token")
    content = input_data.get("content")
    media = input_data.get("media", [])
    
    # Create response
    response = {
        "id": 2,
        "content": content,
        "media": media,
        "status": "created"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()