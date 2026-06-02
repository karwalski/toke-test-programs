import sys
import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

def make_request(url, json_body):
    try:
        data = json_body.encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except:
        return 500

def main():
    # Read input
    url = input().strip()
    concurrent_count = int(input().strip())
    json_body = input().strip()
    
    # Make concurrent requests
    with ThreadPoolExecutor(max_workers=concurrent_count) as executor:
        futures = [executor.submit(make_request, url, json_body) for _ in range(concurrent_count)]
        status_codes = [future.result() for future in futures]
    
    # Count responses by status code
    status_counter = Counter(status_codes)
    
    # Output response distribution
    for status_code in sorted(status_counter.keys()):
        print(f"{status_code}: {status_counter[status_code]}")
    
    # Check for potential race condition (multiple 2xx responses)
    success_count = sum(count for status, count in status_counter.items() if 200 <= status < 300)
    print(f"2xx count: {success_count}")
    
    if success_count > 1:
        print("POTENTIAL RACE CONDITION: Multiple successful responses detected")

if __name__ == "__main__":
    main()