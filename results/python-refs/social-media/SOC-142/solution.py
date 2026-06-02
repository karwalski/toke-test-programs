import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    # Parse JSON input
    try:
        request = json.loads(input_data)
    except json.JSONDecodeError:
        return
    
    # Extract required fields
    action = request.get("action")
    token = request.get("token")
    list_id = request.get("list_id")
    
    # Validate request
    if action != "delete_list" or not token or not list_id:
        return
    
    # For this simple implementation, we'll assume the deletion is always successful
    # In a real system, you would validate the token and check if the list exists
    
    # Create response
    response = {
        "list_id": list_id,
        "status": "deleted"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()