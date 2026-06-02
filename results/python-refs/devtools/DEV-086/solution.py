import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse the JSON array
specs = json.loads(input_data)

# Build the output configuration
config = {"flags": {}}

for spec in specs:
    flag_name = spec["name"]
    config["flags"][flag_name] = {
        "description": spec["description"],
        "enabled": spec["enabled"],
        "rollout_pct": spec["rollout_pct"]
    }

# Output to stdout with no extra whitespace
print(json.dumps(config, separators=(',', ':')))