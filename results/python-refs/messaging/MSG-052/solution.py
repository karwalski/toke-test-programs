import json
import re
import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
user_directory = json.loads(lines[0])
message = lines[1]

# Create username to display name mapping
user_map = {user['username']: user['display'] for user in user_directory}

# Find all @mentions with their positions
mentions = []
unresolved = []
formatted_message = message

# Find all @mentions using regex
pattern = r'@(\w+)'
matches = list(re.finditer(pattern, message))

# Process matches from right to left to maintain positions when replacing
for match in reversed(matches):
    username = match.group(1)
    pos = match.start()
    
    if username in user_map:
        mentions.append((username, pos))
        # Replace @username with display name
        display_name = user_map[username]
        formatted_message = formatted_message[:match.start()] + display_name + formatted_message[match.end():]
    else:
        unresolved.append((username, pos))

# Sort mentions by position for output
mentions.sort(key=lambda x: x[1])
unresolved.sort(key=lambda x: x[1])

# Output results
if mentions:
    mention_parts = [f"{username} (pos {pos})" for username, pos in mentions]
    print("mentions: " + ", ".join(mention_parts))

if unresolved:
    unresolved_parts = [f"{username} (pos {pos})" for username, pos in unresolved]
    print("unresolved: " + ", ".join(unresolved_parts))

print(f"formatted: {formatted_message}")