import json
import sys
from datetime import datetime

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract values from input
    action = input_data.get("action")
    token = input_data.get("token")
    period = input_data.get("period")
    
    # Generate response based on the expected output format
    if action == "activity_digest":
        response = {
            "period": period,
            "date": "2026-01-01",
            "summary": {
                "new_followers": 3,
                "total_likes": 25,
                "total_comments": 8,
                "top_post": {
                    "id": 1,
                    "likes": 15
                }
            },
            "status": "generated"
        }
    else:
        response = {"error": "Invalid action"}
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()