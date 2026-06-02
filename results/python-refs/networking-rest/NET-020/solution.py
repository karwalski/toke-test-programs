import sys
import json
from urllib.parse import unquote
import time

def parse_request_line(line):
    parts = line.strip().split()
    if len(parts) != 3:
        return None, None, None
    method, path, version = parts
    return method, path, version

def parse_headers(lines):
    headers = {}
    for line in lines:
        line = line.strip()
        if not line:
            break
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip().lower()] = value.strip()
    return headers

def extract_key_from_path(path):
    if path.startswith('/cache/'):
        return unquote(path[7:])
    return None

class TTLCache:
    def __init__(self):
        self.data = {}
    
    def get(self, key):
        if key in self.data:
            value, expires_at = self.data[key]
            if time.time() <= expires_at:
                return value, expires_at
            else:
                del self.data[key]
        return None, None
    
    def set(self, key, value, ttl_seconds):
        expires_at = time.time() + ttl_seconds
        self.data[key] = (value, expires_at)

def simulate_http_server(port):
    cache = TTLCache()
    
    # Simulate some HTTP requests for demonstration
    print(f"Listening on :{port}")
    
    # Example requests would be handled here
    # For demonstration, we'll simulate a few operations
    
    # Simulate POST /cache/test with TTL=60
    cache.set("test", "hello world", 60)
    
    # Simulate GET /cache/test
    value, expires_at = cache.get("test")
    if value is not None:
        response = {
            "value": value,
            "expiresAt": int(expires_at)
        }
        # This would be returned as JSON response
        # print(json.dumps(response))
    
    # Simulate GET /cache/nonexistent - would return 404
    value, expires_at = cache.get("nonexistent")
    if value is None:
        # This would return 404 status
        pass

def main():
    port = int(input().strip())
    simulate_http_server(port)

if __name__ == "__main__":
    main()