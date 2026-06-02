import json
import sys
from datetime import datetime, timedelta

def main():
    # Read JSON input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract required fields
    user_id = input_data["user_id"]
    duration_days = input_data["duration_days"]
    reason = input_data["reason"]
    
    # Calculate expiration date (7 days from 2026-01-01)
    base_date = datetime(2026, 1, 1)
    expires_at = base_date + timedelta(days=duration_days)
    expires_at_str = expires_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Create response
    response = {
        "user_id": user_id,
        "suspended": True,
        "duration_days": duration_days,
        "expires_at": expires_at_str,
        "reason": reason,
        "status": "suspended"
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()