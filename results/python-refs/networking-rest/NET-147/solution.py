import sys
import urllib.request
import urllib.parse
import os
import hashlib
import json
import time
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

def get_cache_file(url):
    """Generate cache file path for URL"""
    url_hash = hashlib.md5(url.encode()).hexdigest()
    return f"/tmp/http_cache_{url_hash}.json"

def parse_cache_control(cache_control_header):
    """Parse Cache-Control header and return max-age in seconds"""
    if not cache_control_header:
        return 0
    
    parts = [part.strip() for part in cache_control_header.split(',')]
    for part in parts:
        if part.startswith('max-age='):
            try:
                return int(part.split('=')[1])
            except (ValueError, IndexError):
                pass
        elif part in ['no-cache', 'no-store']:
            return 0
    return 0

def is_cache_fresh(cache_data, current_time):
    """Check if cached response is still fresh"""
    if not cache_data:
        return False
    
    cached_time = cache_data.get('timestamp', 0)
    max_age = cache_data.get('max_age', 0)
    
    if max_age <= 0:
        return False
    
    age = current_time - cached_time
    return age < max_age

def load_cache(cache_file):
    """Load cached response from file"""
    try:
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return None

def save_cache(cache_file, data):
    """Save response to cache file"""
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    except IOError:
        pass

def get_body_summary(body, max_length=50):
    """Get summary of response body"""
    if not body:
        return ""
    
    # Remove extra whitespace and newlines
    summary = ' '.join(body.split())
    
    if len(summary) <= max_length:
        return summary
    
    return summary[:max_length-3] + "..."

def fetch_url(url):
    """Fetch URL with caching support"""
    cache_file = get_cache_file(url)
    current_time = time.time()
    
    # Check cache first
    cache_data = load_cache(cache_file)
    if cache_data and is_cache_fresh(cache_data, current_time):
        status = cache_data.get('status', 200)
        body = cache_data.get('body', '')
        body_summary = get_body_summary(body)
        return f"CACHED {status} {body_summary}".strip()
    
    # Fetch from network
    try:
        with urllib.request.urlopen(url) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='ignore')
            
            # Parse Cache-Control header
            cache_control = response.headers.get('Cache-Control', '')
            max_age = parse_cache_control(cache_control)
            
            # Save to cache if cacheable
            if max_age > 0:
                cache_data = {
                    'status': status,
                    'body': body,
                    'max_age': max_age,
                    'timestamp': current_time
                }
                save_cache(cache_file, cache_data)
            
            body_summary = get_body_summary(body)
            return f"FETCHED {status} {body_summary}".strip()
            
    except Exception as e:
        return f"FETCHED 500 Error: {str(e)}"

def main():
    """Main function to process URLs from stdin"""
    for line in sys.stdin:
        url = line.strip()
        if url:
            result = fetch_url(url)
            print(result)

if __name__ == "__main__":
    main()