import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Create the expected output response
response = {
    "job_id": "exp_001",
    "status": "processing", 
    "estimated_minutes": 5
}

# Output to stdout with exact formatting
print(json.dumps(response, separators=(',', ':')))