import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    post_id = input_data.get("post_id")
    visibility = input_data.get("visibility")
    
    # Validate action
    if action != "set_visibility":
        response = {"error": "Invalid action"}
    # Validate visibility options
    elif visibility not in ["public", "followers", "private"]:
        response = {"error": "Invalid visibility"}
    # Validate required fields
    elif not token or post_id is None or not visibility:
        response = {"error": "Missing required fields"}
    else:
        # Create successful response
        response = {
            "post_id": post_id,
            "visibility": visibility,
            "status": "updated"
        }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()