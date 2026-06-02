import json
import sys

# Read input
block_list = json.loads(input().strip())
messages = json.loads(input().strip())

# Filter messages
filtered_messages = []
blocked_count = 0
blocked_users = set()

for message in messages:
    sender = message["sender"]
    text = message["text"]
    
    if sender in block_list:
        blocked_count += 1
        blocked_users.add(sender)
    else:
        filtered_messages.append(message)

# Output filtered messages
for message in filtered_messages:
    print(f"{message['sender']}: {message['text']}")

# Output blocked message summary
if blocked_count > 0:
    print("---")
    print(f"{blocked_count} messages blocked from {len(blocked_users)} users")