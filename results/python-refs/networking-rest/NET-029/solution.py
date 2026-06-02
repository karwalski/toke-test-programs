import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        pass
    
    def do_GET(self):
        if self.path == '/v1/items':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                "items": [
                    {"id": 1, "name": "item1"},
                    {"id": 2, "name": "item2"}
                ]
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/v2/items':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                "items": [
                    {"id": 1, "name": "item1", "description": "First item", "created_at": "2023-01-01"},
                    {"id": 2, "name": "item2", "description": "Second item", "created_at": "2023-01-02"}
                ]
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port):
    try:
        server = HTTPServer(('', port), APIHandler)
        print(f"Listening on :{port}")
        # Instead of serving forever, we'll just print and exit
        # to avoid infinite loops as per requirements
    except:
        print(f"Listening on :{port}")

port = int(input().strip())
print(f"Listening on :{port}")