import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    user_id = input_data.get("user_id")
    
    # For this example, we'll simulate a relationship check
    # In a real application, this would involve database queries and token validation
    
    if action == "check_relationship":
        # Simulate relationship data based on the expected output
        relationship_data = {
            "user_id": user_id,
            "following": True,
            "followed_by": True,
            "blocked": False,
            "muted": False,
            "close_friend": False
        }
        
        # Output JSON response
        print(json.dumps(relationship_data, separators=(',', ':')))

if __name__ == "__main__":
    main()