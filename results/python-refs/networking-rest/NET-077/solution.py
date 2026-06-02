import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import threading
import time

class VersionedResourceHandler(BaseHTTPRequestHandler):
    # Class variables to store versioned data
    versions = {0: []}  # version 0 starts with empty items
    current_version = 0
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # Check if path matches /v/:version/items
        if len(path_parts) == 3 and path_parts[0] == 'v' and path_parts[2] == 'items':
            try:
                version = int(path_parts[1])
                if version in self.versions:
                    response_data = {
                        "version": version,
                        "items": self.versions[version]
                    }
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response_data).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            except ValueError:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/items':
            # Increment version and copy current items
            self.current_version += 1
            # Copy items from previous version
            prev_items = self.versions[self.current_version - 1].copy()
            self.versions[self.current_version] = prev_items
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response_data = {
                "version": self.current_version,
                "items": self.versions[self.current_version]
            }
            self.wfile.write(json.dumps(response_data).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port):
    server = HTTPServer(('localhost', port), VersionedResourceHandler)
    print(f"Listening on :{port}")
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Let it run briefly then shutdown
    time.sleep(0.1)
    server.shutdown()

# Read port from stdin
port = int(input().strip())
run_server(port)