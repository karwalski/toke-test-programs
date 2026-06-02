import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract notification_id from the request
    notification_id = input_data["notification_id"]
    
    # Create response with exact format
    response = {
        "notification_id": notification_id,
        "status": "deleted"
    }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()