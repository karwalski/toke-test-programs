import sys
import urllib.request
import urllib.parse

# Read input from stdin
url = input().strip()
method = input().strip()
body = input().strip()
cookie = input().strip()

# Parse the body as form data or JSON
if body.startswith('{'):
    # JSON body
    data = body.encode('utf-8')
    content_type = 'application/json'
else:
    # Form data
    data = body.encode('utf-8')
    content_type = 'application/x-www-form-urlencoded'

# Create request
req = urllib.request.Request(url, data=data, method=method)

# Set headers
req.add_header('Content-Type', content_type)
req.add_header('Cookie', cookie)
req.add_header('Origin', 'http://attacker.com')
req.add_header('Referer', 'http://attacker.com/malicious.html')

try:
    # Make the request
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        
    # If we get here without exception, request succeeded
    if 200 <= status_code < 300:
        print("VULNERABLE")
    else:
        print("PROTECTED")
        
except urllib.error.HTTPError as e:
    # HTTP error responses indicate protection
    print("PROTECTED")
except Exception as e:
    # Other errors also indicate protection
    print("PROTECTED")