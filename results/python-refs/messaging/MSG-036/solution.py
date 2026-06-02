import json
from datetime import datetime

# Read input
current_time_str = input().strip()
messages_json = input().strip()

# Parse current time
current_time = datetime.fromisoformat(current_time_str.replace('Z', '+00:00'))

# Parse messages
messages = json.loads(messages_json)

active_messages = []
expired_messages = []

for msg in messages:
    text = msg["text"]
    sent_time = datetime.fromisoformat(msg["sent_time"].replace('Z', '+00:00'))
    ttl_seconds = msg["ttl_seconds"]
    
    # Calculate elapsed time since message was sent
    elapsed_seconds = int((current_time - sent_time).total_seconds())
    
    if elapsed_seconds < ttl_seconds:
        # Message is still active
        remaining_seconds = ttl_seconds - elapsed_seconds
        active_messages.append(f"  {text} ({remaining_seconds}s remaining)")
    else:
        # Message has expired
        expired_seconds = elapsed_seconds - ttl_seconds
        expired_messages.append(f"  {text} (expired {expired_seconds}s ago)")

# Output
print("ACTIVE:")
for msg in active_messages:
    print(msg)
print("EXPIRED:")
for msg in expired_messages:
    print(msg)