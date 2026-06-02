import sys
import json

# Read room name
room_name = input().strip()

# Initialize roster and counters
roster = set()
joins = 0
leaves = 0
kicks = 0

# Process events
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    event = json.loads(line)
    event_type = event["type"]
    user = event["user"]
    
    if event_type == "join":
        roster.add(user)
        joins += 1
    elif event_type == "leave":
        roster.discard(user)
        leaves += 1
    elif event_type == "kick":
        roster.discard(user)
        kicks += 1

# Output final roster (sorted)
for user in sorted(roster):
    print(user)

# Output blank line and summary
print()
print(f"joins: {joins}, leaves: {leaves}, kicks: {kicks}")