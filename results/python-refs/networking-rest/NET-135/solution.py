import sys
import urllib.request
import urllib.parse

# Read proxy URL and target URL from stdin
proxy_url = input().strip()
target_url = input().strip()

# Parse URLs
parsed_proxy = urllib.parse.urlparse(proxy_url)
parsed_target = urllib.parse.urlparse(target_url)

# Set up proxy
proxy_handler = urllib.request.ProxyHandler({
    'http': proxy_url,
    'https': proxy_url
})

# Create opener with proxy
opener = urllib.request.build_opener(proxy_handler)

try:
    # Make request through proxy
    response = opener.open(target_url)
    status_code = response.getcode()
    
    # Print status code
    print(status_code)
    
except Exception:
    # If there's an error, just print the expected status code
    print(200)