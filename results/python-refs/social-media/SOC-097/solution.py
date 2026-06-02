import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract device token and platform from input
device_token = input_data["device_token"]
platform = input_data["platform"]

# Create response
response = {
    "device_token": device_token,
    "platform": platform,
    "status": "registered"
}

# Output JSON response
print(json.dumps(response, separators=(',', ':')))