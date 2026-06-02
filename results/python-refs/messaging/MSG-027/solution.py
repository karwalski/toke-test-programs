import json
import sys
from collections import defaultdict

def main():
    # Read input
    window_size = int(input().strip())
    max_messages = int(input().strip())
    events_json = input().strip()
    events = json.loads(events_json)
    
    # Track message timestamps for each user
    user_messages = defaultdict(list)
    
    # Process each event
    for event in events:
        user = event["user"]
        timestamp = event["time"]
        
        # Remove messages outside the current window
        current_time = timestamp
        window_start = current_time - window_size
        
        # Filter out old messages
        user_messages[user] = [ts for ts in user_messages[user] if ts > window_start]
        
        # Check if we can allow this message
        if len(user_messages[user]) < max_messages:
            user_messages[user].append(timestamp)
            result = "ALLOWED"
        else:
            result = "REJECTED"
        
        # Output result
        print(f"{user}@{timestamp}ms: {result}")

if __name__ == "__main__":
    main()