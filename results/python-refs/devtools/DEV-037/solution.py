import sys
import json

def parse_yaml_simple(text):
    lines = text.strip().split('\n')
    result = {}
    current_key = None
    current_list = None
    
    for line in lines:
        if not line.strip():
            continue
            
        if line.startswith('  - '):
            # List item
            if current_list is not None:
                item = line[4:].strip()
                # Try to convert to number if possible
                try:
                    if '.' in item:
                        item = float(item)
                    else:
                        item = int(item)
                except ValueError:
                    pass
                current_list.append(item)
        elif line.startswith('  '):
            # Nested key (treat as list start for this simple case)
            continue
        else:
            # Top-level key
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                if value:
                    # Simple key-value pair
                    try:
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass
                    result[key] = value
                else:
                    # Key with no immediate value (likely a list follows)
                    current_list = []
                    result[key] = current_list
                    current_key = key
    
    return result

# Read from stdin
input_text = sys.stdin.read()

# Parse YAML
data = parse_yaml_simple(input_text)

# Convert to JSON with proper formatting
json_output = json.dumps(data, indent=2, sort_keys=True)
print(json_output)