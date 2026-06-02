import sys
import json
import re

def parse_yaml_simple(yaml_content):
    lines = yaml_content.strip().split('\n')
    result = {}
    current_list = None
    current_key = None
    
    for line in lines:
        line = line.rstrip()
        if not line:
            continue
            
        # Handle list items
        if line.startswith('  - '):
            item = line[4:]
            if current_list is not None:
                current_list.append(item)
            continue
            
        # Handle key-value pairs
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if value:
                # Try to convert to int
                if value.isdigit():
                    result[key] = int(value)
                else:
                    result[key] = value
                current_list = None
            else:
                # This key has a list value
                result[key] = []
                current_list = result[key]
                current_key = key
                
    return result

# Read input from stdin
yaml_content = sys.stdin.read()

# Parse YAML
data = parse_yaml_simple(yaml_content)

# Output as pretty-printed JSON
print(json.dumps(data, indent=2, sort_keys=True))