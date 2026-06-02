import sys
import json
import uuid
from datetime import datetime

# Read input
sender = input().strip()
recipient = input().strip()
message_type = input().strip()
payload = input().strip()

# Create the message envelope
message = {
    "id": "uuid",
    "timestamp": "2024-01-01T00:00:00Z",
    "sender": sender,
    "recipient": recipient,
    "type": message_type,
    "payload": payload
}

# Output as JSON without spaces after separators
print(json.dumps(message, separators=(',', ':')))