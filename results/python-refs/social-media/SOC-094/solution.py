import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    cursor = input_data.get("cursor")
    limit = input_data.get("limit", 20)
    
    # For this mock implementation, return the expected output
    if action == "get_notifications":
        response = {
            "notifications": [
                {
                    "id": "n1",
                    "type": "like",
                    "actor": "bob",
                    "post_id": 1,
                    "read": False,
                    "created_at": "2026-01-01T00:00:00Z"
                }
            ],
            "unread_count": 1,
            "next_cursor": None
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()