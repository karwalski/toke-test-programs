import json
import sys

# Read range specifications
ranges = {}
for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    parts = line.split()
    field = parts[0]
    min_val = float(parts[1])
    max_val = float(parts[2])
    ranges[field] = (min_val, max_val)

# Process JSON objects
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    obj = json.loads(line)
    violations = []
    
    # Check each field that has a range specification
    for field, (min_val, max_val) in ranges.items():
        if field in obj:
            value = obj[field]
            if not (min_val <= value <= max_val):
                violations.append(f"{field}={value} (expected {int(min_val)}-{int(max_val)})")
    
    if violations:
        print("INVALID: " + ", ".join(violations))
    else:
        print(json.dumps(obj, separators=(',', ':')))