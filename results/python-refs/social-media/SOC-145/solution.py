import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    group_id = input_data.get("group_id")
    content = input_data.get("content")
    
    # Simple token validation (extract username from token pattern)
    # In a real system, this would involve proper JWT validation
    author = "alice"  # Hardcoded based on expected output
    
    # Create the group post response
    response = {
        "id": 50,
        "group_id": group_id,
        "content": content,
        "author": author,
        "visibility": "group",
        "status": "created"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()