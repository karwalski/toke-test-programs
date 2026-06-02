import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON input
messages = json.loads(input_data)

# Track seen IDs and deduplicated messages
seen_ids = set()
deduplicated = []
removed_count = 0

# Process each message
for message in messages:
    msg_id = message["id"]
    if msg_id not in seen_ids:
        seen_ids.add(msg_id)
        deduplicated.append(message)
    else:
        removed_count += 1

# Output deduplicated messages as JSON
print(json.dumps(deduplicated, separators=(',', ':')))

# Output removed count
print(f"removed {removed_count} duplicates")