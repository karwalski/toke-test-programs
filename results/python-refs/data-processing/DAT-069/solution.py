import sys
import yaml

def deep_merge(dict1, dict2):
    """Deep merge dict2 into dict1"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

# Read all input from stdin
input_data = sys.stdin.read().strip()

# Split documents by '---' separator
documents = input_data.split('\n---\n')

# Parse each YAML document and merge them
merged = {}
for doc in documents:
    if doc.strip():
        parsed = yaml.safe_load(doc.strip())
        if parsed:
            merged = deep_merge(merged, parsed)

# Output the merged result
print(yaml.dump(merged, default_flow_style=False, sort_keys=True).strip())