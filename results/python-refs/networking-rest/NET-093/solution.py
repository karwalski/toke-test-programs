import sys
from urllib.parse import parse_qs
import time
from datetime import datetime, timedelta
import re

def parse_cache_control(cache_control_header):
    """Parse Cache-Control header into directives"""
    if not cache_control_header:
        return {}
    
    directives = {}
    parts = [part.strip() for part in cache_control_header.split(',')]
    
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            try:
                directives[key.strip()] = int(value.strip())
            except ValueError:
                directives[key.strip()] = value.strip()
        else:
            directives[part.strip()] = True
    
    return directives

def should_cache_response(cache_control):
    """Determine if response should be cached based on Cache-Control directives"""
    if 'no-store' in cache_control:
        return False
    if 'private' in cache_control:
        return False
    return True

def is_response_fresh(cache_control, age_seconds):
    """Check if cached response is still fresh"""
    if 'no-cache' in cache_control:
        return False
    
    if 'must-revalidate' in cache_control and age_seconds > 0:
        # Check if max-age has been exceeded
        if 'max-age' in cache_control:
            return age_seconds <= cache_control['max-age']
        return False
    
    if 's-maxage' in cache_control:
        return age_seconds <= cache_control['s-maxage']
    
    if 'max-age' in cache_control:
        return age_seconds <= cache_control['max-age']
    
    return True

def simulate_http_server(port):
    """Simulate HTTP server behavior with cache control"""
    print(f"Listening on :{port}")
    
    # Simulate some cached responses with different cache control scenarios
    cache = {}
    current_time = time.time()
    
    # Example scenarios would be handled here in a real server
    # For the simulation, we just show the server is listening
    
    return

def main():
    port = int(input().strip())
    simulate_http_server(port)

if __name__ == "__main__":
    main()