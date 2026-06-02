import sys
import json
import re

# Read pattern specifications
patterns = {}
for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    parts = line.split(' ', 1)
    field = parts[0]
    regex = parts[1]
    patterns[field] = re.compile(regex)

# Process JSON objects
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        obj = json.loads(line)
        invalid_fields = []
        
        # Check each field against its pattern
        for field, pattern in patterns.items():
            if field in obj:
                value = str(obj[field])
                if not pattern.match(value):
                    invalid_fields.append(f"{field}={value} (does not match pattern)")
        
        if invalid_fields:
            print("INVALID: " + ", ".join(invalid_fields))
        else:
            print(json.dumps(obj, separators=(',', ':')))
    
    except json.JSONDecodeError:
        continue