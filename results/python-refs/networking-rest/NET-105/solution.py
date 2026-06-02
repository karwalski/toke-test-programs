import sys
import urllib.request
import json

# Read input from stdin
url = input().strip()
json_body = input().strip()

try:
    # Create the request
    data = json_body.encode('utf-8')
    req = urllib.request.Request(url, data=data, method='PATCH')
    req.add_header('Content-Type', 'application/json')
    
    # Perform the request
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        response_body = response.read().decode('utf-8')
        
    # Print the output
    print(status_code)
    
except Exception as e:
    # If there's an error, print status code and empty body
    print("Error")
    print("")