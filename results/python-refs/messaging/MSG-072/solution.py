import json
import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
rules = json.loads(lines[0])
messages = json.loads(lines[1])

# Apply migration rules to each message
migrated_messages = []

for message in messages:
    new_message = message.copy()
    
    # Apply remove rules first
    if 'remove' in rules:
        for field in rules['remove']:
            if field in new_message:
                del new_message[field]
    
    # Apply rename rules
    if 'rename' in rules:
        for old_field, new_field in rules['rename'].items():
            if old_field in new_message:
                new_message[new_field] = new_message[old_field]
                del new_message[old_field]
    
    # Apply add rules
    if 'add' in rules:
        for field, default_value in rules['add'].items():
            new_message[field] = default_value
    
    migrated_messages.append(new_message)

# Output result
print(json.dumps(migrated_messages, separators=(',', ':')))