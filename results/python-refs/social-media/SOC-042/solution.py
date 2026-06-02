import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract preferences from input
    preferences = input_data.get("preferences", {})
    
    # Create response with saved preferences
    response = {
        "preferences": preferences,
        "status": "saved"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()