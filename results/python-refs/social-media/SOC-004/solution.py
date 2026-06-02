import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract fields from input
    action = input_data.get("action")
    token = input_data.get("token")
    bio = input_data.get("bio", "")
    display_name = input_data.get("display_name", "")
    avatar_url = input_data.get("avatar_url", "")
    
    # Simple authentication check (token exists)
    if not token:
        response = {"error": "Authentication required"}
    elif action == "update_profile":
        # Create response with updated profile
        response = {
            "id": 1,
            "bio": bio,
            "display_name": display_name,
            "status": "updated"
        }
        
        # Only include avatar_url in response if it was provided in input
        if "avatar_url" in input_data:
            response["avatar_url"] = avatar_url
    else:
        response = {"error": "Invalid action"}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()