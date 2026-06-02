import json
import sys

def json_to_yaml(data, indent=0):
    result = []
    spaces = "  " * indent
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                result.append(f"{spaces}{key}:")
                result.append(json_to_yaml(value, indent + 1))
            else:
                result.append(f"{spaces}{key}: {json_to_yaml(value, 0)}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                result.append(f"{spaces}- ")
                sub_yaml = json_to_yaml(item, indent + 1)
                # Replace the first indentation with "- " for the first line
                lines = sub_yaml.split('\n')
                if lines:
                    first_line = lines[0].lstrip()
                    result[-1] += first_line
                    result.extend(lines[1:])
            else:
                result.append(f"{spaces}- {json_to_yaml(item, 0)}")
    else:
        return str(data)
    
    return '\n'.join(result)

# Read JSON from stdin
json_input = sys.stdin.read().strip()
data = json.loads(json_input)

# Convert to YAML and print
yaml_output = json_to_yaml(data)
print(yaml_output)