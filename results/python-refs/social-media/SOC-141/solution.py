import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract action and token
    action = input_data.get("action")
    token = input_data.get("token")
    
    # Simulate authentication and data retrieval
    # In a real application, you would validate the token and query a database
    if action == "my_lists" and token:
        # Mock data for the authenticated user
        response = {
            "owned": [
                {
                    "id": "lst_1",
                    "name": "Tech Leaders",
                    "member_count": 5
                }
            ],
            "subscribed": [
                {
                    "id": "lst_2",
                    "name": "News Sources",
                    "owner": "bob",
                    "member_count": 20
                }
            ]
        }
    else:
        response = {"error": "Invalid action or token"}
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()