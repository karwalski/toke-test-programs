import json
import sys

def reconstruct_nested_json(flat_obj):
    result = {}
    
    for key, value in flat_obj.items():
        # Split the key by dots to get the path
        parts = key.split('.')
        
        # Navigate/create the nested structure
        current = result
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the final value
        current[parts[-1]] = value
    
    return result

# Read input from stdin
input_str = sys.stdin.read().strip()
flat_obj = json.loads(input_str)

# Reconstruct the nested object
nested_obj = reconstruct_nested_json(flat_obj)

# Output with exact formatting to match expected output
print(json.dumps(nested_obj, indent=2, sort_keys=True))