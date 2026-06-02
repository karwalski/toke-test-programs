import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Read URL from stdin
url = input().strip()

try:
    # Create DELETE request
    request = Request(url, method='DELETE')
    
    # Perform the request
    with urlopen(request) as response:
        status_code = response.getcode()
        print(status_code)

except HTTPError as e:
    status_code = e.code
    print(status_code)

except URLError as e:
    print(f"Error: {e}")