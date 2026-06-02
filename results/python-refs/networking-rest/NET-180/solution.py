#!/usr/bin/env python3

import sys
import json
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

def log_to_stderr(timestamp, method, url, status, latency):
    log_entry = {
        "timestamp": timestamp,
        "method": method,
        "url": url,
        "status": status,
        "latency": latency
    }
    print(json.dumps(log_entry), file=sys.stderr)

def make_request(method, url, body=None):
    start_time = time.time()
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(start_time))
    
    try:
        if body:
            data = body.encode('utf-8')
            req = Request(url, data=data, method=method)
            req.add_header('Content-Type', 'application/json')
        else:
            req = Request(url, method=method)
        
        with urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            status = response.getcode()
            latency = round((time.time() - start_time) * 1000, 2)
            
            log_to_stderr(timestamp, method, url, status, latency)
            print(response_body)
            
    except HTTPError as e:
        latency = round((time.time() - start_time) * 1000, 2)
        log_to_stderr(timestamp, method, url, e.code, latency)
        response_body = e.read().decode('utf-8')
        print(response_body)
        
    except URLError as e:
        latency = round((time.time() - start_time) * 1000, 2)
        log_to_stderr(timestamp, method, url, 0, latency)

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' ', 2)
        method = parts[0]
        url = parts[1]
        body = parts[2] if len(parts) > 2 else None
        
        make_request(method, url, body)

if __name__ == "__main__":
    main()