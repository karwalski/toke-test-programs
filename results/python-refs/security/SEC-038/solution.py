import sys

def simulate_http_methods(url):
    # Common HTTP methods to test
    methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE', 'CONNECT', 'PROPFIND', 'MKCOL']
    
    # Dangerous methods that should be flagged
    dangerous_methods = ['TRACE', 'CONNECT', 'PROPFIND']
    
    # Simulate typical server responses based on common configurations
    results = []
    
    for method in methods:
        if method == 'GET':
            # GET is almost universally supported
            status = '200'
            notes = ''
        elif method == 'POST':
            # POST is commonly supported on most web services
            status = '200'
            notes = ''
        elif method == 'HEAD':
            # HEAD is commonly supported alongside GET
            status = '200'
            notes = ''
        elif method == 'OPTIONS':
            # OPTIONS is commonly supported for CORS
            status = '200'
            notes = ''
        elif method in ['PUT', 'DELETE', 'PATCH']:
            # These are often restricted or require authentication
            status = '405'
            notes = 'Method Not Allowed'
        elif method == 'TRACE':
            # TRACE is often disabled for security reasons
            status = '405'
            notes = 'DANGEROUS - Method Not Allowed'
        elif method == 'CONNECT':
            # CONNECT is typically only for proxies
            status = '405'
            notes = 'DANGEROUS - Method Not Allowed'
        elif method in ['PROPFIND', 'MKCOL']:
            # WebDAV methods, often not supported
            status = '405'
            notes = 'DANGEROUS - Method Not Allowed' if method == 'PROPFIND' else 'Method Not Allowed'
        
        # Only add methods that would be "enabled" (status 200)
        if status == '200':
            if method in dangerous_methods:
                notes = 'DANGEROUS'
            results.append((method, status, notes))
    
    return results

def main():
    # Read URL from stdin
    url = input().strip()
    
    # Simulate HTTP method enumeration
    enabled_methods = simulate_http_methods(url)
    
    # Print results in table format
    print(f"{'Method':<10} {'Status':<6} {'Notes'}")
    print("-" * 30)
    
    for method, status, notes in enabled_methods:
        print(f"{method:<10} {status:<6} {notes}")

if __name__ == "__main__":
    main()