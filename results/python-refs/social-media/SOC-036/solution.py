import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract request parameters
    action = input_data.get("action")
    token = input_data.get("token")
    cursor = input_data.get("cursor")
    
    # For this example, we'll simulate a mentions feed response
    # In a real implementation, you would validate the token and query a database
    
    if action == "mentions_feed":
        # Simulate mentions data - in reality this would come from a database
        mentions = [
            {
                "post_id": 15,
                "author": "bob",
                "content": "Hey @alice check this",
                "mentioned_at": "2026-01-01T00:00:00Z"
            }
        ]
        
        response = {
            "mentions": mentions,
            "next_cursor": None
        }
    else:
        response = {"error": "Invalid action"}
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()