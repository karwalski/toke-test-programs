import socket
import threading
import time
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import URLError
import json

class CircuitBreaker:
    def __init__(self, failure_threshold, timeout=5):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise e

class MockDownstream(BaseHTTPRequestHandler):
    fail_mode = False
    
    def do_GET(self):
        if MockDownstream.fail_mode:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Internal Server Error')
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
    
    def log_message(self, format, *args):
        pass

class ProxyHandler(BaseHTTPRequestHandler):
    circuit_breaker = None
    downstream_url = None
    
    def do_GET(self):
        try:
            def make_request():
                response = urlopen(self.downstream_url, timeout=1)
                return response.read()
            
            result = self.circuit_breaker.call(make_request)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(result)
        except Exception:
            self.send_response(503)
            self.end_headers()
            self.wfile.write(b'Service Unavailable')
    
    def log_message(self, format, *args):
        pass

def start_server(port, handler_class):
    server = HTTPServer(('localhost', port), handler_class)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def make_request(proxy_port):
    try:
        response = urlopen(f'http://localhost:{proxy_port}', timeout=1)
        return response.getcode()
    except Exception:
        return 503

def test_phase(name, proxy_port, expected_status):
    status = make_request(proxy_port)
    passed = status == expected_status
    print(f"{name}: {'PASS' if passed else 'FAIL'}")
    return passed

def main():
    proxy_port = int(input().strip())
    downstream_port = int(input().strip())
    failure_threshold = int(input().strip())
    
    # Setup circuit breaker
    circuit_breaker = CircuitBreaker(failure_threshold)
    ProxyHandler.circuit_breaker = circuit_breaker
    ProxyHandler.downstream_url = f'http://localhost:{downstream_port}'
    
    # Start servers
    downstream_server = start_server(downstream_port, MockDownstream)
    proxy_server = start_server(proxy_port, ProxyHandler)
    
    time.sleep(0.1)  # Let servers start
    
    # Test Normal phase
    test_phase("Normal", proxy_port, 200)

if __name__ == "__main__":
    main()