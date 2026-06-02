import json
import sys
from datetime import datetime, timezone

def parse_iso_time(iso_string):
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))

def format_time_diff(seconds):
    if seconds == 0:
        return "due now"
    elif seconds < 0:
        # Past due
        abs_seconds = abs(seconds)
        if abs_seconds < 60:
            return f"was due {abs_seconds}s ago"
        elif abs_seconds < 3600:
            minutes = abs_seconds // 60
            return f"was due {minutes}m ago"
        else:
            hours = abs_seconds // 3600
            return f"was due {hours}h ago"
    else:
        # Future
        if seconds < 60:
            return f"in {seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"in {minutes}m"
        else:
            hours = seconds // 3600
            return f"in {hours}h"

# Read input
current_time_str = input().strip()
messages_json_str = input().strip()

# Parse input
current_time = parse_iso_time(current_time_str)
messages = json.loads(messages_json_str)

# Process messages
ready_messages = []
pending_messages = []

for msg in messages:
    deliver_time = parse_iso_time(msg['deliver_at'])
    time_diff = int((deliver_time - current_time).total_seconds())
    
    msg_info = {
        'text': msg['text'],
        'sender': msg['sender'],
        'recipient': msg['recipient'],
        'deliver_time': deliver_time,
        'time_diff': time_diff,
        'time_str': format_time_diff(time_diff)
    }
    
    if time_diff <= 0:
        ready_messages.append(msg_info)
    else:
        pending_messages.append(msg_info)

# Sort by delivery time
ready_messages.sort(key=lambda x: x['deliver_time'])
pending_messages.sort(key=lambda x: x['deliver_time'])

# Output
print("READY:")
for msg in ready_messages:
    print(f"  {msg['sender']}->{msg['recipient']}: {msg['text']} ({msg['time_str']})")

print("PENDING:")
for msg in pending_messages:
    print(f"  {msg['sender']}->{msg['recipient']}: {msg['text']} ({msg['time_str']})")