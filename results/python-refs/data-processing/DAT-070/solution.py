import json
import sys

def get_all_paths(obj, prefix=""):
    """Get all paths and their values from a JSON object."""
    paths = {}
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, (dict, list)):
                paths.update(get_all_paths(value, new_prefix))
            else:
                paths[new_prefix] = value
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            new_prefix = f"{prefix}[{i}]" if prefix else f"[{i}]"
            if isinstance(value, (dict, list)):
                paths.update(get_all_paths(value, new_prefix))
            else:
                paths[new_prefix] = value
    else:
        paths[prefix] = obj
    
    return paths

def format_value(value):
    """Format a value for output."""
    if isinstance(value, str):
        return value
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return "null"
    else:
        return str(value)

# Read input
input_text = sys.stdin.read().strip()
parts = input_text.split('\n\n')

json_a = json.loads(parts[0])
json_b = json.loads(parts[1])

# Get all paths for both JSON documents
paths_a = get_all_paths(json_a)
paths_b = get_all_paths(json_b)

# Find differences
changes = []
additions = []
removals = []

# Check for changes and removals
for path, value_a in paths_a.items():
    if path in paths_b:
        value_b = paths_b[path]
        if value_a != value_b:
            changes.append((path, value_a, value_b))
    else:
        removals.append((path, value_a))

# Check for additions
for path, value_b in paths_b.items():
    if path not in paths_a:
        additions.append((path, value_b))

# Sort all changes by path for consistent output
changes.sort()
removals.sort()
additions.sort()

# Output results
for path, old_val, new_val in changes:
    print(f"~ {path}: {format_value(old_val)} -> {format_value(new_val)}")

for path, value in removals:
    print(f"- {path}: {format_value(value)}")

for path, value in additions:
    print(f"+ {path}: {format_value(value)}")