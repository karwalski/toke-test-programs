import json
import sys

# Read input
members = json.loads(input().strip())
receipts = json.loads(input().strip())

# Aggregate read receipts by message ID
message_readers = {}
for receipt in receipts:
    msg_id = receipt["msg_id"]
    user = receipt["user"]
    if msg_id not in message_readers:
        message_readers[msg_id] = set()
    message_readers[msg_id].add(user)

# Process each message
for msg_id in sorted(message_readers.keys()):
    readers = message_readers[msg_id]
    non_readers = set(members) - readers
    
    read_count = len(readers)
    total_count = len(members)
    
    print(f"{msg_id}: {read_count}/{total_count} read")
    print(f"  read: {', '.join(sorted(readers))}")
    print(f"  unread: {', '.join(sorted(non_readers))}")