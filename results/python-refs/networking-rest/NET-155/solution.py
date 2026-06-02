import urllib.request
import urllib.error
import sys

def main():
    # Read input from stdin
    url = input().strip()
    expected_status = int(input().strip())
    timeout = int(input().strip())
    
    try:
        # Make HTTP request
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            actual_status = response.getcode()
            
            if actual_status == expected_status:
                print("HEALTHY")
                sys.exit(0)
            else:
                print(f"UNHEALTHY: Expected status {expected_status}, got {actual_status}")
                sys.exit(1)
                
    except urllib.error.HTTPError as e:
        actual_status = e.code
        if actual_status == expected_status:
            print("HEALTHY")
            sys.exit(0)
        else:
            print(f"UNHEALTHY: Expected status {expected_status}, got {actual_status}")
            sys.exit(1)
            
    except urllib.error.URLError as e:
        print(f"UNHEALTHY: {e.reason}")
        sys.exit(1)
        
    except Exception as e:
        print(f"UNHEALTHY: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()