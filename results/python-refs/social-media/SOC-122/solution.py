import json
import sys
from datetime import datetime

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    action = input_data.get("action")
    token = input_data.get("token")
    limit = input_data.get("limit", 10)
    
    if action != "network_trends":
        response = {"error": "Invalid action"}
    else:
        # Mock network trends data based on the expected output format
        trends = [
            {
                "topic": "rust programming",
                "network_posts": 50,
                "participants": ["alice", "bob", "carol"],
                "started_at": "2026-01-01T10:00:00Z"
            }
        ]
        
        # Apply limit
        trends = trends[:limit]
        
        response = {"trends": trends}
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()