import json
import sys

# Read the field name from the first line
field_name = input().strip()

# Initialize counters
total_lines = 0
valid_lines = 0
invalid_lines = 0
field_missing = 0
extracted_values = []

# Process each line from stdin
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    total_lines += 1
    
    try:
        # Try to parse JSON
        json_obj = json.loads(line)
        valid_lines += 1
        
        # Check if field exists
        if field_name in json_obj:
            extracted_values.append(str(json_obj[field_name]))
        else:
            field_missing += 1
            
    except json.JSONDecodeError:
        # Invalid JSON
        invalid_lines += 1

# Output extracted values
for value in extracted_values:
    print(value)

# Output summary
print("---")
print(f"Total: {total_lines}, Valid: {valid_lines}, Invalid: {invalid_lines}, Field missing: {field_missing}")