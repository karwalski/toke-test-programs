import sys
import urllib.request
import urllib.error
import concurrent.futures
from threading import Thread
import queue

def fetch_url(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8', errors='ignore')
            first_line = body.split('\n')[0][:100]
            return url, status, first_line
    except Exception:
        return url, 0, ""

def main():
    urls = []
    for line in sys.stdin:
        url = line.strip()
        if url:
            urls.append(url)
    
    if not urls:
        return
    
    # Use ThreadPoolExecutor for concurrent fetching
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in urls}
        
        for future in concurrent.futures.as_completed(future_to_url, timeout=8):
            url, status, first_line = future.result()
            results[url] = (status, first_line)
    
    # Output in input order
    for url in urls:
        if url in results:
            status, first_line = results[url]
            print(f"{url} {status} {first_line}")
        else:
            print(f"{url} 0 ")

if __name__ == "__main__":
    main()