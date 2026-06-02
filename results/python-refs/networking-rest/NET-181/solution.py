import sys
import urllib.request
import urllib.error
import socket

def main():
    # Read URL and timeout from stdin
    url = input().strip()
    timeout_ms = int(input().strip())
    timeout_seconds = timeout_ms / 1000.0
    
    try:
        # Set socket timeout
        socket.setdefaulttimeout(timeout_seconds)
        
        # Fetch the URL
        with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
            if response.status == 200:
                print("200")
                sys.exit(0)
            else:
                print(f"ERROR: HTTP {response.status}")
                sys.exit(1)
                
    except socket.timeout:
        print(f"TIMEOUT after {timeout_ms}ms")
        sys.exit(1)
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print(f"TIMEOUT after {timeout_ms}ms")
        else:
            print(f"ERROR: {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()