import json
import sys

# Read the field path from the first line
field_path = input().strip()

# Parse the field path (remove leading dot and split by dots)
if field_path.startswith('.'):
    field_path = field_path[1:]

fields = field_path.split('.') if field_path else []

# Process each JSON line
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        obj = json.loads(line)
        
        # Navigate through the field path
        current = obj
        for field in fields:
            if isinstance(current, dict) and field in current:
                current = current[field]
            else:
                current = None
                break
        
        # Output the result if found
        if current is not None:
            if isinstance(current, str):
                print(current)
            else:
                print(json.dumps(current, separators=(',', ':')))
    
    except (json.JSONDecodeError, KeyError, TypeError):
        # Skip invalid JSON or missing fields
        continue