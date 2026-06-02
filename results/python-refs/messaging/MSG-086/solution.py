import json
import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
fields_to_strip = json.loads(lines[0])
message = json.loads(lines[1])

# Strip the specified fields and track what was removed
stripped_fields = []
for field in fields_to_strip:
    if field in message:
        del message[field]
        stripped_fields.append(field)

# Output the result
print(json.dumps(message, separators=(',', ':')))
print(f"stripped: {', '.join(stripped_fields)}")