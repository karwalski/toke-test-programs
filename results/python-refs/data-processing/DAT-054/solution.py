import json
import sys

def flatten_json(obj, parent_key='', sep='.'):
    """
    Flatten a nested json object using dot notation for keys.
    """
    items = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(flatten_json(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
    else:
        return {parent_key: obj}
    
    return dict(items)

# Read JSON from stdin
input_data = sys.stdin.read().strip()
json_obj = json.loads(input_data)

# Flatten the JSON object
flattened = flatten_json(json_obj)

# Output as JSON with sorted keys to match expected format
print(json.dumps(flattened, sort_keys=True, separators=(',', ':')))