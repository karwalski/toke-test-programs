import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        accept_header = self.headers.get('Accept', '')
        
        if 'application/vnd.api.v1+json' in accept_header:
            self.send_response(200)
            self.send_header('Content-Type', 'application/vnd.api.v1+json')
            self.end_headers()
            response = {'version': 'v1', 'data': {'message': 'Hello from API v1'}}
            self.wfile.write(json.dumps(response).encode())
        elif 'application/vnd.api.v2+json' in accept_header:
            self.send_response(200)
            self.send_header('Content-Type', 'application/vnd.api.v2+json')
            self.end_headers()
            response = {'version': 'v2', 'data': {'message': 'Hello from API v2', 'features': ['enhanced']}}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(406)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': 'Not Acceptable', 'message': 'Supported versions: v1, v2'}
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        pass

def start_server(port):
    server = HTTPServer(('localhost', port), APIHandler)
    server.timeout = 1
    server.serve_request()

port = int(input().strip())
print(f"Listening on :{port}")

# Simulate server behavior without infinite loop
def server_thread():
    try:
        start_server(port)
    except:
        pass

thread = threading.Thread(target=server_thread, daemon=True)
thread.start()
time.sleep(0.1)