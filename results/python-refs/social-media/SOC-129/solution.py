import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    # Parse JSON input
    request = json.loads(input_data)
    
    # Extract required fields
    action = request.get("action")
    token = request.get("token")
    message_id = request.get("message_id")
    for_everyone = request.get("for_everyone")
    
    # Process delete message request
    if action == "delete_message":
        # Determine deletion scope
        deleted_for = "everyone" if for_everyone else "self"
        
        # Create response
        response = {
            "message_id": message_id,
            "deleted_for": deleted_for,
            "status": "deleted"
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()