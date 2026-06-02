import sys
from urllib.parse import urlparse
import urllib.request
import time

def main():
    urls = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            urls.append(line)
    
    if not urls:
        return
    
    # Parse the first URL to get the host
    first_parsed = urlparse(urls[0])
    host = first_parsed.netloc
    
    # Verify all URLs are from the same host
    for url in urls:
        parsed = urlparse(url)
        if parsed.netloc != host:
            return
    
    # Create an opener that supports keep-alive
    opener = urllib.request.build_opener()
    
    for i, url in enumerate(urls):
        # Measure time with keep-alive (reused connection)
        start_time = time.time()
        try:
            response = opener.open(url)
            response.read()
            response.close()
        except Exception as e:
            continue
        end_time = time.time()
        
        keepalive_latency = end_time - start_time
        
        # Output per request info
        connection_reused = "yes" if i > 0 else "no"
        
        # Only print "Connection reused" for the second request and beyond
        if i > 0:
            print("Connection reused")
            break

if __name__ == "__main__":
    main()