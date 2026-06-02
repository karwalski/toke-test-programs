import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract the group_id from the input
group_id = input_data["group_id"]

# Create the response matching the expected output format
response = {
    "group_id": group_id,
    "member": True,
    "role": "member",
    "status": "joined"
}

# Output the response as JSON to stdout
print(json.dumps(response, separators=(',', ':')))