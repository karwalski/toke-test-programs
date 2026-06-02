import sys
import json
import re

def parse_toml(content):
    result = {}
    current_section = None
    
    lines = content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Section header
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            if current_section not in result:
                result[current_section] = {}
            continue
        
        # Key-value pair
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Parse value
            if value.startswith('"') and value.endswith('"'):
                # String value
                parsed_value = value[1:-1]
            elif value.isdigit():
                # Integer value
                parsed_value = int(value)
            else:
                # Default to string
                parsed_value = value
            
            if current_section:
                result[current_section][key] = parsed_value
            else:
                result[key] = parsed_value
    
    return result

# Read from stdin
content = sys.stdin.read()

# Parse TOML
parsed = parse_toml(content)

# Output as pretty-printed JSON
print(json.dumps(parsed, indent=2, sort_keys=True))