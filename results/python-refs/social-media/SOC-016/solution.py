import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract fields from input
    action = input_data.get("action")
    token = input_data.get("token")
    content = input_data.get("content")
    tags = input_data.get("tags", [])
    visibility = input_data.get("visibility")
    
    # Create response object
    response = {
        "id": 1,
        "content": content,
        "tags": tags,
        "visibility": visibility,
        "created_at": "2026-01-01T00:00:00Z",
        "status": "created"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()