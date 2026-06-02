import sys
import urllib.request
import urllib.parse
import json

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

if len(lines) < 2:
    print("Error: Need at least URL and query")
    sys.exit(1)

url = lines[0]
query = ''.join(lines[1:])

# Prepare the GraphQL request
data = {
    "query": query
}

# Convert to JSON and encode
json_data = json.dumps(data).encode('utf-8')

# Create the request
req = urllib.request.Request(
    url,
    data=json_data,
    headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
)

try:
    # Send the request
    with urllib.request.urlopen(req) as response:
        response_data = response.read().decode('utf-8')
        response_json = json.loads(response_data)
        
    # Pretty print the response
    print(json.dumps(response_json, indent=2))
    
except urllib.error.HTTPError as e:
    error_data = e.read().decode('utf-8')
    try:
        error_json = json.loads(error_data)
        print(json.dumps(error_json, indent=2))
    except:
        print(f"HTTP Error {e.code}: {error_data}")
        
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
    
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")
    
except Exception as e:
    print(f"Error: {e}")