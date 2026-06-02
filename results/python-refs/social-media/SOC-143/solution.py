import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract fields from input
    action = input_data.get("action")
    token = input_data.get("token")
    name = input_data.get("name")
    description = input_data.get("description")
    rules = input_data.get("rules")
    private = input_data.get("private")
    
    # Simple validation - check if required fields are present
    if action == "create_group" and token and name:
        # Create response with group object
        response = {
            "group_id": "grp_1",
            "name": name,
            "description": description,
            "member_count": 1,
            "status": "created"
        }
    else:
        # Handle error case
        response = {
            "error": "Invalid request"
        }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()