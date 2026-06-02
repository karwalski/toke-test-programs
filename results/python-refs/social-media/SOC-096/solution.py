import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract preferences from the input
preferences = input_data.get("preferences", {})

# Create the response
response = {
    "preferences": preferences,
    "status": "saved"
}

# Output the response as JSON
print(json.dumps(response, separators=(',', ':')))