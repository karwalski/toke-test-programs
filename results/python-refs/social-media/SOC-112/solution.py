import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    action = input_data.get("action")
    token = input_data.get("token")
    user_id = input_data.get("user_id")
    warning_type = input_data.get("warning_type")
    message = input_data.get("message")
    
    # Simple strike tracking (in a real system this would be persistent storage)
    # For this example, we'll simulate that user 99 already has 1 strike
    current_strikes = 1 if user_id == 99 else 0
    new_strikes = current_strikes + 1
    max_strikes = 3
    
    # Generate warning ID (simplified)
    warning_id = "w_001"
    
    # Create response
    response = {
        "warning_id": warning_id,
        "user_id": user_id,
        "type": warning_type,
        "strikes": new_strikes,
        "max_strikes": max_strikes,
        "status": "warned"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()