import sys
from urllib.parse import urlparse, parse_qs

def check_open_redirect(url):
    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        # Parameters to check for open redirect
        redirect_params = ['redirect_uri', 'next', 'url', 'return_to']
        
        for param in redirect_params:
            if param in query_params:
                redirect_values = query_params[param]
                for redirect_url in redirect_values:
                    try:
                        redirect_parsed = urlparse(redirect_url)
                        # Check if redirect URL has a different domain
                        if redirect_parsed.netloc and redirect_parsed.netloc != parsed.netloc:
                            return f"VULNERABLE to {redirect_url} via {param}"
                    except:
                        continue
        
        return "SAFE"
    except:
        return "SAFE"

# Read URLs from stdin
for line in sys.stdin:
    url = line.strip()
    if url:
        result = check_open_redirect(url)
        if result.startswith("VULNERABLE"):
            print("VULNERABLE")
        else:
            print("SAFE")