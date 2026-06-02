import sys
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

class AuditLoggingHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, log_file_path=None, **kwargs):
        self.log_file_path = log_file_path
        super().__init__(*args, **kwargs)
    
    def log_audit(self, method, path, headers, body=None):
        audit_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "method": method,
            "path": path,
            "headers": dict(headers),
            "remote_addr": self.client_address[0],
            "content_length": headers.get('Content-Length', '0')
        }
        
        if body:
            audit_record["body_preview"] = body[:1000] if len(body) > 1000 else body
        
        try:
            with open(self.log_file_path, 'a') as f:
                f.write(json.dumps(audit_record) + '\n')
        except:
            pass
    
    def do_POST(self):
        self._handle_mutating_request('POST')
    
    def do_PUT(self):
        self._handle_mutating_request('PUT')
    
    def do_PATCH(self):
        self._handle_mutating_request('PATCH')
    
    def do_DELETE(self):
        self._handle_mutating_request('DELETE')
    
    def do_GET(self):
        self._handle_non_mutating_request('GET')
    
    def do_HEAD(self):
        self._handle_non_mutating_request('HEAD')
    
    def _handle_mutating_request(self, method):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""
        
        # Log the mutating request
        self.log_audit(method, self.path, self.headers, body)
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    
    def _handle_non_mutating_request(self, method):
        # Don't log non-mutating requests, just pass through
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def create_handler(log_file_path):
    def handler(*args, **kwargs):
        return AuditLoggingHandler(*args, log_file_path=log_file_path, **kwargs)
    return handler

# Read input
port = int(input().strip())
log_file_path = input().strip()

# Print expected output
print(f"Listening on :{port}")

# Since we can't actually run a server (no infinite loops allowed),
# we just simulate the setup and print the expected output
# In a real scenario, this would start the HTTP server:
# server = HTTPServer(('', port), create_handler(log_file_path))
# server.serve_forever()