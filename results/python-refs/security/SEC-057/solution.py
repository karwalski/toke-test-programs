import sys
import urllib.request
import urllib.parse
import time

def measure_login_time(url, username, password="wrongpassword"):
    """Measure the response time for a login attempt"""
    data = urllib.parse.urlencode({'username': username, 'password': password})
    data = data.encode('ascii')
    
    start_time = time.time()
    try:
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req, timeout=10)
        response.read()
    except:
        pass
    end_time = time.time()
    
    return (end_time - start_time) * 1000  # Convert to milliseconds

def main():
    # Read input
    url = input().strip()
    valid_user = input().strip()
    invalid_user = input().strip()
    
    # Measure timing for valid username (with wrong password)
    valid_times = []
    for _ in range(5):
        timing = measure_login_time(url, valid_user)
        valid_times.append(timing)
    
    # Measure timing for invalid username
    invalid_times = []
    for _ in range(5):
        timing = measure_login_time(url, invalid_user)
        invalid_times.append(timing)
    
    # Calculate averages
    valid_avg = sum(valid_times) / len(valid_times)
    invalid_avg = sum(invalid_times) / len(invalid_times)
    
    # Output results
    print("valid_user_avg:")

if __name__ == "__main__":
    main()