import sys
import urllib.request
import urllib.error
import time
from concurrent.futures import ThreadPoolExecutor
import threading

def make_request(url):
    """Make a single request and return status code"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 500

def fire_rapid_requests(url, num_requests):
    """Fire requests rapidly and count responses"""
    results = {'200': 0, '429': 0, '5xx': 0}
    
    # Use ThreadPoolExecutor to fire requests rapidly
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, url) for _ in range(num_requests)]
        
        for future in futures:
            status = future.result()
            if status == 200:
                results['200'] += 1
            elif status == 429:
                results['429'] += 1
            elif status >= 500:
                results['5xx'] += 1

    return results

def assess_protection(results, num_requests, expected_limit):
    """Assess if rate limiting is properly enforced"""
    total_success = results['200']
    rate_limited = results['429']
    
    # If we got significant rate limiting (429s), it's protected
    if rate_limited > 0:
        return "PROTECTED"
    
    # If we got way more successes than the expected limit, likely unprotected
    if total_success > expected_limit * 2:
        return "UNPROTECTED"
    
    # If we got close to or under the expected limit, likely protected
    if total_success <= expected_limit * 1.5:
        return "PROTECTED"
    
    return "UNPROTECTED"

def main():
    # Read input
    url = input().strip()
    num_requests = int(input().strip())
    expected_limit = int(input().strip())
    
    # Fire rapid requests
    results = fire_rapid_requests(url, num_requests)
    
    # Assess protection
    assessment = assess_protection(results, num_requests, expected_limit)
    
    print(assessment)

if __name__ == "__main__":
    main()