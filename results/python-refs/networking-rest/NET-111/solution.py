import sys
import urllib.request
import urllib.error
import time
import datetime

def main():
    # Read input
    url = input().strip()
    max_wait = int(input().strip())
    expected_status = int(input().strip())
    
    start_time = time.time()
    delay = 1  # Start with 1 second delay
    attempt = 0
    
    while time.time() - start_time < max_wait:
        attempt += 1
        
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()
                
                if status_code == expected_status:
                    print("PASS")
                    return
                    
        except urllib.error.HTTPError as e:
            status_code = e.code
            
            if status_code == expected_status:
                print("PASS")
                return
                
        except Exception as e:
            pass
        
        # Check if we have time for another attempt
        if time.time() - start_time + delay >= max_wait:
            break
            
        # Wait with exponential backoff
        time.sleep(delay)
        delay = min(delay * 2, 16)  # Cap at 16 seconds
    
    print("FAIL")

if __name__ == "__main__":
    main()