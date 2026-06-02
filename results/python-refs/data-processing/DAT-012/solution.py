import sys
import json

# Read mapping rules
mapping = {}
for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    old_field, new_field = line.split(':', 1)
    if new_field == '-':
        mapping[old_field] = None  # Mark for deletion
    else:
        mapping[old_field] = new_field

# Process JSON objects
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    obj = json.loads(line)
    new_obj = {}
    
    for old_key, value in obj.items():
        if old_key in mapping:
            new_key = mapping[old_key]
            if new_key is not None:  # Not marked for deletion
                new_obj[new_key] = value
        else:
            new_obj[old_key] = value  # Keep unmapped fields as-is
    
    print(json.dumps(new_obj, separators=(',', ':')))