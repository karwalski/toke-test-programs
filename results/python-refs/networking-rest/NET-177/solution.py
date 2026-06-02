import sys
import urllib.request
import urllib.error

def main():
    # Read URL from stdin
    url = input().strip()
    
    try:
        # Create OPTIONS request
        req = urllib.request.Request(url, method='OPTIONS')
        
        # Send the request
        with urllib.request.urlopen(req) as response:
            headers = response.headers
            
            # Get Allow header
            allow_header = headers.get('Allow', '')
            print(f"Allow: {allow_header}")
            
            # Get CORS headers
            cors_headers = {}
            for header_name, header_value in headers.items():
                if header_name.lower().startswith('access-control-'):
                    cors_headers[header_name] = header_value
            
            # Print CORS headers if present
            for header_name, header_value in cors_headers.items():
                print(f"{header_name}: {header_value}")
                
    except (urllib.error.URLError, urllib.error.HTTPError, Exception):
        # If request fails, output empty Allow header
        print("Allow:")

if __name__ == "__main__":
    main()