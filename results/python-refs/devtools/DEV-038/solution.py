import json
import sys

def json_to_yaml(obj, indent=0):
    if isinstance(obj, dict):
        result = []
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                result.append(' ' * indent + f'{key}:')
                result.append(json_to_yaml(value, indent + 2))
            else:
                result.append(' ' * indent + f'{key}: {value}')
        return '\n'.join(result)
    elif isinstance(obj, list):
        result = []
        for item in obj:
            if isinstance(item, (dict, list)):
                result.append(' ' * indent + '-')
                result.append(json_to_yaml(item, indent + 2))
            else:
                result.append(' ' * indent + f'- {item}')
        return '\n'.join(result)
    else:
        return str(obj)

json_input = sys.stdin.read().strip()
data = json.loads(json_input)
yaml_output = json_to_yaml(data)
print(yaml_output)