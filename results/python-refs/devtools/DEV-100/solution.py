import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
records = json.loads(input_data)

# Build dependency map
dependency_map = {}
for record in records:
    caller = record["caller"]
    callee = record["callee"]
    call_count = record["call_count"]
    
    if caller not in dependency_map:
        dependency_map[caller] = []
    
    dependency_map[caller].append((callee, call_count))

# Sort services alphabetically and output
for service in sorted(dependency_map.keys()):
    print(f"{service}:")
    for callee, call_count in dependency_map[service]:
        print(f"  -> {callee} ({call_count} calls)")