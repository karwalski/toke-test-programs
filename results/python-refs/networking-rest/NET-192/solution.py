import sys
import urllib.request
import urllib.parse
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_page(url, page):
    try:
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        query_params['page'] = [str(page)]
        new_query = urllib.parse.urlencode(query_params, doseq=True)
        new_url = urllib.parse.urlunparse((
            parsed_url.scheme, parsed_url.netloc, parsed_url.path,
            parsed_url.params, new_query, parsed_url.fragment
        ))
        
        with urllib.request.urlopen(new_url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return page, data
    except:
        return page, None

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    base_url = lines[0]
    concurrency = int(lines[1])
    
    start_time = time.time()
    
    # First, determine how many pages exist
    max_pages = 100  # Start with reasonable estimate
    all_items = []
    page_data = {}
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit jobs for pages 1 to max_pages
        future_to_page = {executor.submit(fetch_page, base_url, page): page 
                         for page in range(1, max_pages + 1)}
        
        for future in future_to_page:
            page, data = future.result()
            if data and len(data) > 0:
                page_data[page] = data
                all_items.extend(data)
    
    end_time = time.time()
    
    # Find actual page range
    if page_data:
        min_page = min(page_data.keys())
        max_page = max(page_data.keys())
        
        # Check for gaps
        gaps = 0
        for page in range(min_page, max_page + 1):
            if page not in page_data:
                gaps += 1
    else:
        gaps = 0
    
    # Check for duplicates
    seen_items = set()
    duplicates = 0
    for item in all_items:
        item_str = json.dumps(item, sort_keys=True)
        if item_str in seen_items:
            duplicates += 1
        else:
            seen_items.add(item_str)
    
    total_items = len(all_items)
    time_taken = round(end_time - start_time, 2)
    
    print(f"Total items:")

if __name__ == "__main__":
    main()