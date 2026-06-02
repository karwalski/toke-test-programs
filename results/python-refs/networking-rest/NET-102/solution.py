import sys
import urllib.request
import urllib.parse
import json

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

if not lines:
    sys.exit(1)

url = lines[0]
json_body = '\n'.join(lines[1:]) if len(lines) > 1 else ''

try:
    # Create the request
    data = json_body.encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    # Make the request
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        response_body = response.read().decode('utf-8')
    
    # Print output
    print(status_code)
    print(response_body, end='')
    
except Exception as e:
    print("Error")