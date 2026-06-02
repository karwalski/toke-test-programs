import json
import sys

# Read input
line1 = input().strip()
line2 = input().strip()

# Parse JSON arrays
client_versions = json.loads(line1)
server_versions = json.loads(line2)

# Find common versions
common_versions = set(client_versions) & set(server_versions)

if not common_versions:
    print("INCOMPATIBLE")
else:
    # Find highest version (assuming semantic versioning)
    # Convert to tuples for proper comparison
    def version_to_tuple(v):
        return tuple(map(int, v.split('.')))
    
    # Sort common versions and get the highest
    sorted_versions = sorted(common_versions, key=version_to_tuple, reverse=True)
    negotiated_version = sorted_versions[0]
    
    print(negotiated_version)
    response = {"status": "ok", "version": negotiated_version}
    print(json.dumps(response, separators=(',', ':')))