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
    private = input_data.get("private")
    
    # Create response based on action
    if action == "create_list":
        response = {
            "list_id": "lst_1",
            "name": name,
            "description": description,
            "private": private,
            "member_count": 0,
            "status": "created"
        }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()