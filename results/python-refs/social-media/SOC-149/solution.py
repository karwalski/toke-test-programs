import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    request = json.loads(input_data)
    
    # Create the response
    response = {
        "webhook_id": "wh_1",
        "url": request["url"],
        "events": request["events"],
        "secret": "whsec_abc123",
        "status": "active"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()