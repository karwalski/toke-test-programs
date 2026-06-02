import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone

def create_har_entry(url, request_time, response_time, status_code, headers, content):
    """Create a HAR entry for a single request/response"""
    return {
        "startedDateTime": request_time.isoformat(),
        "time": (response_time - request_time).total_seconds() * 1000,
        "request": {
            "method": "GET",
            "url": url,
            "httpVersion": "HTTP/1.1",
            "headers": [],
            "queryString": [],
            "cookies": [],
            "headersSize": -1,
            "bodySize": 0
        },
        "response": {
            "status": status_code,
            "statusText": "OK" if status_code == 200 else "Error",
            "httpVersion": "HTTP/1.1",
            "headers": [{"name": k, "value": v} for k, v in headers.items()],
            "cookies": [],
            "content": {
                "size": len(content),
                "mimeType": headers.get("Content-Type", "text/html"),
                "text": content
            },
            "redirectURL": "",
            "headersSize": -1,
            "bodySize": len(content)
        },
        "cache": {},
        "timings": {
            "blocked": 0,
            "dns": 0,
            "connect": 0,
            "send": 0,
            "wait": 100,
            "receive": 0,
            "ssl": -1
        }
    }

def main():
    # Read output file path
    output_path = input().strip()
    
    # Read URLs
    urls = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            urls.append(line)
        except EOFError:
            break
    
    # Create HAR structure
    har = {
        "log": {
            "version": "1.2",
            "creator": {
                "name": "Python HAR Generator",
                "version": "1.0"
            },
            "entries": []
        }
    }
    
    # Fetch each URL and create HAR entries
    for url in urls:
        try:
            request_time = datetime.now(timezone.utc)
            
            # Fetch the URL
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                response_time = datetime.now(timezone.utc)
                content = response.read().decode('utf-8', errors='ignore')
                headers = dict(response.headers)
                status_code = response.getcode()
                
                entry = create_har_entry(url, request_time, response_time, status_code, headers, content)
                har["log"]["entries"].append(entry)
                
        except Exception:
            # Create a minimal error entry
            response_time = datetime.now(timezone.utc)
            entry = create_har_entry(url, request_time, response_time, 0, {}, "")
            har["log"]["entries"].append(entry)
    
    # Write HAR file
    with open(output_path, 'w') as f:
        json.dump(har, f, indent=2)
    
    # Print result
    num_entries = len(har["log"]["entries"])
    print(f"HAR written to {output_path} with {num_entries} entries")

if __name__ == "__main__":
    main()