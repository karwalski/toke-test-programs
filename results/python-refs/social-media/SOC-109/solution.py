import json
import sys
from datetime import datetime

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract parameters
    action = input_data.get("action")
    token = input_data.get("token")
    date_from = input_data.get("date_from")
    date_to = input_data.get("date_to")
    limit = input_data.get("limit")
    
    # Mock moderation log data
    mock_entries = [
        {
            "id": "ml_1",
            "moderator": "mod_user",
            "action": "remove",
            "target_post": 99,
            "reason": "spam",
            "at": "2026-01-01T00:00:00Z"
        }
    ]
    
    # Filter entries based on date range if provided
    filtered_entries = []
    if date_from and date_to:
        for entry in mock_entries:
            entry_date = entry["at"][:10]  # Extract YYYY-MM-DD part
            if date_from <= entry_date <= date_to:
                filtered_entries.append(entry)
    else:
        filtered_entries = mock_entries
    
    # Apply limit if specified
    if limit and len(filtered_entries) > limit:
        filtered_entries = filtered_entries[:limit]
    
    # Create response
    response = {
        "entries": filtered_entries,
        "total": len(filtered_entries)
    }
    
    # Output JSON response
    print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()