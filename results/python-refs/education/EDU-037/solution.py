import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

required_connections = input_data["required"]
actual_connections = input_data["actual"]

# Convert actual connections to a set of tuples for easy lookup
actual_set = set()
for conn in actual_connections:
    actual_set.add((conn["from"], conn["to"], conn["label"]))

# Check for missing connections
missing = []
for req_conn in required_connections:
    req_tuple = (req_conn["from"], req_conn["to"], req_conn["label"])
    if req_tuple not in actual_set:
        missing.append(f"MISSING: {req_conn['from']} -> {req_conn['to']} ({req_conn['label']})")

# Output result
if not missing:
    print("PASS")
else:
    for miss in missing:
        print(miss)