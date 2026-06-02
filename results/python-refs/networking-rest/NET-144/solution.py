import sys
import urllib.request
import urllib.error
import time

def check_url(url):
    try:
        start_time = time.time()
        
        # Create a request with proper headers
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0')
        
        # Open the URL and follow redirects automatically
        response = urllib.request.urlopen(request, timeout=5)
        
        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)
        
        status_code = response.getcode()
        final_url = response.geturl()
        
        return status_code, final_url, response_time_ms
        
    except urllib.error.HTTPError as e:
        end_time = time.time()
        response_time_ms = int((end_time - start_time) * 1000)
        return e.code, url, response_time_ms
        
    except Exception:
        return None, url, 0

def main():
    first_url = True
    for line in sys.stdin:
        url = line.strip()
        if url:
            status, final_url, response_time = check_url(url)
            if status is not None and first_url:
                print(status)
                first_url = False

if __name__ == "__main__":
    main()