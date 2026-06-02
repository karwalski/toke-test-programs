import json
import os
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
env_specs = json.loads(input_data)

# Process each environment variable spec
for spec in env_specs:
    name = spec["name"]
    required = spec["required"]
    default = spec["default"]
    
    # Check if the environment variable is set
    value = os.environ.get(name)
    
    if value is not None:
        # Variable is set
        print(f"{name}: SET ({value})")
    elif required:
        # Variable is missing and required
        print(f"{name}: MISSING")
    else:
        # Variable is missing but not required, use default
        print(f"{name}: USING DEFAULT ({default})")