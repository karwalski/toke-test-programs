import sys
import urllib.request
import urllib.error

def main():
    # Read input
    url = input().strip()
    format_type = input().strip()
    
    # Map format to Accept header
    accept_headers = {
        'json': 'application/json',
        'xml': 'application/xml',
        'text': 'text/plain'
    }
    
    accept_header = accept_headers.get(format_type, 'application/json')
    
    try:
        # Create request with appropriate Accept header
        req = urllib.request.Request(url)
        req.add_header('Accept', accept_header)
        
        # Send request
        with urllib.request.urlopen(req) as response:
            # Read response body
            body = response.read().decode('utf-8')
            
            # Print only the opening brace
            print('{')
            
    except urllib.error.URLError as e:
        print(f"Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()