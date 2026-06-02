import json
import sys
from datetime import datetime

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Collect all messages with channel information
all_messages = []
channel_counts = {}

for channel, messages in input_data.items():
    channel_counts[channel] = len(messages)
    for message in messages:
        message['channel'] = channel
        all_messages.append(message)

# Sort messages by time
all_messages.sort(key=lambda msg: datetime.fromisoformat(msg['time'].replace('Z', '+00:00')))

# Output unified inbox
for message in all_messages:
    time_obj = datetime.fromisoformat(message['time'].replace('Z', '+00:00'))
    time_str = time_obj.strftime('%H:%M')
    print(f"[{time_str}] [{message['channel']}] {message['sender']}: {message['text']}")

print("---")

# Output channel counts
total = sum(channel_counts.values())
count_parts = []
for channel in sorted(channel_counts.keys()):
    count_parts.append(f"{channel}: {channel_counts[channel]}")
count_parts.append(f"total: {total}")

print(", ".join(count_parts))