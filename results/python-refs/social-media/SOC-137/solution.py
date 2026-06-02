import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    request = json.loads(input_data)
    
    # Extract required fields
    list_id = request["list_id"]
    user_id = request["user_id"]
    
    # Create response
    response = {
        "list_id": list_id,
        "user_id": user_id,
        "member_count": 1,
        "status": "added"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()