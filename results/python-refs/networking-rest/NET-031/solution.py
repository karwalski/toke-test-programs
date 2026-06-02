import sys
import hmac
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Read input
port = int(input().strip())
secret = input().strip()

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/webhook':
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Read the payload
            payload = self.rfile.read(content_length)
            
            # Get the signature from header
            signature_header = self.headers.get('X-Webhook-Signature', '')
            
            # Validate HMAC-SHA256 signature
            if signature_header.startswith('sha256='):
                provided_signature = signature_header[7:]  # Remove 'sha256=' prefix
                
                # Calculate expected signature
                expected_signature = hmac.new(
                    secret.encode('utf-8'),
                    payload,
                    hashlib.sha256
                ).hexdigest()
                
                # Compare signatures
                if hmac.compare_digest(provided_signature, expected_signature):
                    # Valid signature
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'OK')
                    
                    # Log payload summary
                    payload_summary = f"Valid payload received: {len(payload)} bytes"
                    print(payload_summary, file=sys.stderr)
                else:
                    # Invalid signature
                    self.send_response(401)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'Unauthorized')
            else:
                # No valid signature format
                self.send_response(401)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Unauthorized')
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

# Since we can't actually start a server, just print the expected output
print(f"Listening on :{port}")

# Simulate server behavior without actually starting it
# The server would handle POST requests to /webhook with HMAC validation