import sys
import json

def parse_yaml_simple(yaml_text):
    """Simple YAML parser for basic key-value pairs"""
    result = {}
    
    for line in yaml_text.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Try to convert to int
            try:
                value = int(value)
            except ValueError:
                # Try to convert to float
                try:
                    value = float(value)
                except ValueError:
                    # Keep as string, remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
            
            result[key] = value
    
    return result

# Read from stdin
yaml_input = sys.stdin.read()

# Parse YAML
data = parse_yaml_simple(yaml_input)

# Convert to JSON with pretty printing
json_output = json.dumps(data, indent=2, sort_keys=True)

# Print to stdout
print(json_output)