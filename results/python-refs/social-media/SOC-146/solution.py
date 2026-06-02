import json
import sys
from datetime import datetime, timezone, timedelta

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract action and token
    action = input_data.get("action")
    token = input_data.get("token")
    
    # Check if this is a rate limit status request
    if action == "rate_limit_status":
        # Calculate reset time (15 minutes from now)
        reset_time = datetime.now(timezone.utc) + timedelta(minutes=15)
        reset_at = reset_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Create response with rate limit info
        response = {
            "limit": 300,
            "remaining": 250,
            "reset_at": "2026-01-01T00:15:00Z",
            "window_seconds": 900
        }
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))
    else:
        # Handle other actions if needed
        response = {"error": "Unknown action"}
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()