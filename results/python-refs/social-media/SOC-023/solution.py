import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    content = input_data.get("content")
    scheduled_at = input_data.get("scheduled_at")
    
    # Create response for scheduled post
    if action == "schedule_post":
        response = {
            "id": 4,
            "content": content,
            "scheduled_at": scheduled_at,
            "status": "scheduled"
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()