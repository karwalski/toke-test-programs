import json
import sys

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    try:
        # Parse JSON input
        request = json.loads(input_data)
        
        # Check if this is a deactivation request with confirmation
        if (request.get("action") == "deactivate" and 
            request.get("confirm") == True and 
            request.get("token")):
            
            # Return success response with exact format
            response = {
                "status": "deactivated",
                "reactivation_window_days": 30
            }
            
            # Output JSON with no extra whitespace
            print(json.dumps(response, separators=(',', ':')))
        
        else:
            # Invalid request
            response = {"status": "error", "message": "Invalid request"}
            print(json.dumps(response, separators=(',', ':')))
            
    except json.JSONDecodeError:
        # Invalid JSON
        response = {"status": "error", "message": "Invalid JSON"}
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()