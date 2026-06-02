import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import threading
import time
from queue import Queue

def read_sitemap_urls(url_or_path):
    """Read URLs from XML sitemap"""
    urls = []
    try:
        if url_or_path.startswith('http'):
            with urllib.request.urlopen(url_or_path) as response:
                content = response.read()
        else:
            with open(url_or_path, 'r') as f:
                content = f.read().encode()
        
        root = ET.fromstring(content)
        # Handle namespace
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url_elem in root.findall('.//sitemap:url/sitemap:loc', namespace):
            urls.append(url_elem.text.strip())
        
        # If no namespaced elements found, try without namespace
        if not urls:
            for url_elem in root.findall('.//url/loc'):
                urls.append(url_elem.text.strip())
                
    except Exception:
        pass
    
    return urls

def read_url_list(file_path):
    """Read URLs from plain text file"""
    urls = []
    try:
        if file_path.startswith('http'):
            with urllib.request.urlopen(file_path) as response:
                content = response.read().decode('utf-8')
                urls = [line.strip() for line in content.splitlines() if line.strip()]
        else:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
    except Exception:
        pass
    
    return urls

def fetch_url(url, results):
    """Fetch a single URL and determine cache status"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            headers = response.headers
            
            # Check various cache headers to determine if it was a hit or miss
            cache_status = 'miss'  # default to miss (warmed)
            
            # Common cache headers that indicate a hit
            cache_headers = [
                'x-cache', 'x-cache-status', 'cf-cache-status', 
                'x-served-by', 'x-cache-lookup', 'cache-control'
            ]
            
            for header in cache_headers:
                value = headers.get(header, '').lower()
                if 'hit' in value or 'cached' in value:
                    cache_status = 'hit'
                    break
                elif 'miss' in value:
                    cache_status = 'miss'
                    break
            
            results.append(('success', cache_status))
    except Exception:
        results.append(('error', None))

def main():
    # Read input
    source_type = input().strip()
    url_or_path = input().strip()
    concurrency = int(input().strip())
    
    # Get URLs based on source type
    if source_type == 'sitemap':
        urls = read_sitemap_urls(url_or_path)
    else:  # list
        urls = read_url_list(url_or_path)
    
    if not urls:
        print("Warming")
        return
    
    print("Warming")
    
    # Process URLs concurrently
    results = []
    threads = []
    semaphore = threading.Semaphore(concurrency)
    
    def worker(url):
        with semaphore:
            fetch_url(url, results)
    
    # Start all threads
    for url in urls:
        thread = threading.Thread(target=worker, args=(url,))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Count results
    total_urls = len(urls)
    warmed = sum(1 for r in results if r[0] == 'success' and r[1] == 'miss')
    already_hot = sum(1 for r in results if r[0] == 'success' and r[1] == 'hit')
    errors = sum(1 for r in results if r[0] == 'error')
    
    # Output final stats
    print(f"Total URLs: {total_urls}, Warmed: {warmed}, Already hot: {already_hot}, Errors: {errors}")

if __name__ == "__main__":
    main()