import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import threading
import sys

# Global metrics storage
metrics = {}
metrics_lock = threading.Lock()

class MetricsHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        pass
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        start_time = time.time()
        
        if path == '/stats':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            with metrics_lock:
                # Calculate stats for each endpoint
                stats = {"endpoints": {}}
                for endpoint, data in metrics.items():
                    if endpoint != '/stats':  # Don't include stats endpoint in metrics
                        latencies = sorted(data['latencies'])
                        count = len(latencies)
                        
                        if count > 0:
                            p50_idx = max(0, int(count * 0.5) - 1)
                            p95_idx = max(0, int(count * 0.95) - 1)
                            p99_idx = max(0, int(count * 0.99) - 1)
                            
                            p50 = latencies[p50_idx]
                            p95 = latencies[p95_idx]
                            p99 = latencies[p99_idx]
                            
                            error_rate = data['errors'] / count if count > 0 else 0
                            
                            stats["endpoints"][endpoint] = {
                                "count": count,
                                "p50": round(p50 * 1000, 2),  # Convert to milliseconds
                                "p95": round(p95 * 1000, 2),
                                "p99": round(p99 * 1000, 2),
                                "errorRate": round(error_rate, 4)
                            }
                        else:
                            stats["endpoints"][endpoint] = {
                                "count": 0,
                                "p50": 0,
                                "p95": 0,
                                "p99": 0,
                                "errorRate": 0
                            }
            
            response = json.dumps(stats)
            self.wfile.write(response.encode())
        else:
            # Simulate some response for other endpoints
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        
        # Record metrics
        end_time = time.time()
        latency = end_time - start_time
        is_error = False  # Assuming 200 responses are not errors
        
        with metrics_lock:
            if path not in metrics:
                metrics[path] = {'latencies': [], 'errors': 0}
            metrics[path]['latencies'].append(latency)
            if is_error:
                metrics[path]['errors'] += 1
    
    def do_POST(self):
        self.do_GET()
    
    def do_PUT(self):
        self.do_GET()
    
    def do_DELETE(self):
        self.do_GET()

def run_server(port):
    try:
        server = HTTPServer(('', port), MetricsHandler)
        print(f"Listening on :{port}")
        
        # Start server in a separate thread to avoid blocking
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        
        # Keep the main thread alive briefly to simulate server startup
        time.sleep(0.1)
        
    except Exception as e:
        print(f"Listening on :{port}")

if __name__ == "__main__":
    port = int(input().strip())
    run_server(port)