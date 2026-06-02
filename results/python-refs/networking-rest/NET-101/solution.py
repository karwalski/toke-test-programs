import sys
import urllib.request
import urllib.error

# Read URL from stdin
url = input().strip()

try:
    # Perform HTTP GET request
    with urllib.request.urlopen(url) as response:
        # Print status code
        print(response.getcode())

except urllib.error.HTTPError as e:
    # Print error status code
    print(e.code)

except urllib.error.URLError as e:
    # Handle network errors
    print("Error:", str(e))

except Exception as e:
    # Handle other errors
    print("Error:", str(e))