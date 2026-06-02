import json
import sys

# Read input
timeout_ms = int(input().strip())
events_json = input().strip()
events = json.loads(events_json)

# Sort events by time
events.sort(key=lambda x: x['time'])

# Track typing users and their last activity
typing_users = {}  # user -> last_activity_time
output_times = set()

# Collect all event times for output
for event in events:
    output_times.add(event['time'])

# Process events and generate output
for event_time in sorted(output_times):
    # Process all events at this time
    for event in events:
        if event['time'] == event_time:
            user = event['user']
            event_type = event['type']
            
            if event_type == 'start' or event_type == 'keystroke':
                typing_users[user] = event_time
            elif event_type == 'stop':
                if user in typing_users:
                    del typing_users[user]
    
    # Remove users who have timed out
    current_typing = []
    for user, last_activity in typing_users.items():
        if event_time - last_activity < timeout_ms:
            current_typing.append(user)
        else:
            # Will be removed in next iteration
            pass
    
    # Update typing_users to remove timed out users
    typing_users = {user: time for user, time in typing_users.items() 
                   if event_time - time < timeout_ms}
    
    # Sort users for consistent output
    current_typing.sort()
    
    # Output
    print(f"{event_time}ms: {current_typing}")