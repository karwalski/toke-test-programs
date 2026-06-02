import sys
import json
from datetime import datetime, timezone

def main():
    output_path = input().strip()
    urls = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            urls.append(line)
        except EOFError:
            break
    
    har = {
        "log": {
            "version": "1.2",
            "creator": {"name": "Python HAR Generator", "version": "1.0"},
            "entries": []
        }
    }
    
    now = datetime.now(timezone.utc).isoformat()
    for url in urls:
        entry = {
            "startedDateTime": now,
            "time": 100,
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
                "status": 0,
                "statusText": "",
                "httpVersion": "HTTP/1.1",
                "headers": [],
                "cookies": [],
                "content": {"size": 0, "mimeType": "text/html", "text": ""},
                "redirectURL": "",
                "headersSize": -1,
                "bodySize": 0
            },
            "cache": {},
            "timings": {"blocked": 0, "dns": 0, "connect": 0, "send": 0, "wait": 100, "receive": 0, "ssl": -1}
        }
        har["log"]["entries"].append(entry)
    
    try:
        with open(output_path, 'w') as f:
            json.dump(har, f, indent=2)
    except Exception:
        pass
    
    print("HAR written")

if __name__ == "__main__":
    main()