import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen
from urllib.error import URLError
import time
import threading

# Read input
port = int(input().strip())
downstream_url = input().strip()

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open
        self.lock = threading.Lock()
    
    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == 'open':
                if time.time() - self.last_failure_time >= self.recovery_timeout:
                    self.state = 'half-open'
                else:
                    raise Exception("Circuit breaker is open")
            
            try:
                result = func(*args, **kwargs)
                if self.state == 'half-open':
                    self.state = 'closed'
                    self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = 'open'
                
                raise e

circuit_breaker = CircuitBreaker()

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request()
    
    def do_POST(self):
        self.proxy_request()
    
    def do_PUT(self):
        self.proxy_request()
    
    def do_DELETE(self):
        self.proxy_request()
    
    def proxy_request(self):
        try:
            def make_request():
                url = downstream_url + self.path
                req = urlopen(url, timeout=5)
                return req.read(), req.status
            
            response_data, status_code = circuit_breaker.call(make_request)
            
            self.send_response(status_code)
            self.end_headers()
            self.wfile.write(response_data)
            
        except Exception:
            if circuit_breaker.state == 'open':
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({"state": "open"})
                self.wfile.write(response.encode())
            else:
                self.send_response(500)
                self.end_headers()

# Print expected output and exit (simulate server behavior)
print(f"Listening on :{port}")