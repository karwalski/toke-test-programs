import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract session_id from the request
    session_id = input_data.get("session_id")
    
    # Create response
    response = {
        "status": "revoked",
        "session_id": session_id
    }
    
    # Output JSON response to stdout
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()