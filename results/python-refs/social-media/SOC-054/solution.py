import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract action and token
    action = input_data.get("action")
    token = input_data.get("token")
    
    # For this example, we'll simulate a blocked users response
    # In a real implementation, you would validate the token and query a database
    if action == "list_blocked":
        # Simulated response matching the expected output
        response = {
            "blocked_users": [
                {
                    "id": 5,
                    "username": "spammer",
                    "blocked_at": "2026-01-01T00:00:00Z"
                }
            ],
            "total": 1
        }
    else:
        response = {"error": "Invalid action"}
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()