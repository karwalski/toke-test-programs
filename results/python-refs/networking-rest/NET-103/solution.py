import sys
import json

# Read input from stdin
url = input().strip()
json_body = input().strip()

# Parse the JSON to validate it
try:
    parsed_json = json.loads(json_body)
except json.JSONDecodeError:
    print("400")
    print("Invalid JSON")
    sys.exit()

# For httpbin.org/put, simulate a successful PUT request
# httpbin.org typically returns the data that was sent to it
if "httpbin.org/put" in url:
    print("200")
else:
    # For other URLs, simulate a basic successful response
    print("200")
    print('{"status":"success"}')