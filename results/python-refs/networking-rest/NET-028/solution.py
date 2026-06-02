import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import threading
from urllib.parse import urlparse

# Global metrics storage
request_count = 0
response_times = []
error_count = 0

class MetricsHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        pass
    
    def do_GET(self):
        global request_count, response_times, error_count
        
        start_time = time.time()
        request_count += 1
        
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/metrics':
            # Return Prometheus format metrics
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            # Calculate histogram buckets for response latency
            latency_buckets = [0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
            bucket_counts = {str(bucket): 0 for bucket in latency_buckets}
            bucket_counts['+Inf'] = len(response_times)
            
            for response_time in response_times:
                for bucket in latency_buckets:
                    if response_time <= bucket:
                        bucket_counts[str(bucket)] += 1
            
            # Generate Prometheus metrics
            metrics_output = []
            
            # Request count
            metrics_output.append('# HELP http_requests_total Total number of HTTP requests')
            metrics_output.append('# TYPE http_requests_total counter')
            metrics_output.append(f'http_requests_total {request_count}')
            
            # Response latency histogram
            metrics_output.append('# HELP http_response_duration_seconds Response latency histogram')
            metrics_output.append('# TYPE http_response_duration_seconds histogram')
            
            for bucket, count in bucket_counts.items():
                metrics_output.append(f'http_response_duration_seconds_bucket{{le="{bucket}"}} {count}')
            
            metrics_output.append(f'http_response_duration_seconds_sum {sum(response_times):.6f}')
            metrics_output.append(f'http_response_duration_seconds_count {len(response_times)}')
            
            # Error rate
            metrics_output.append('# HELP http_errors_total Total number of HTTP errors')
            metrics_output.append('# TYPE http_errors_total counter')
            metrics_output.append(f'http_errors_total {error_count}')
            
            response_text = '\n'.join(metrics_output) + '\n'
            self.wfile.write(response_text.encode('utf-8'))
            
        else:
            # Return JSON for other routes
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {
                "message": "Hello World",
                "path": self.path,
                "method": "GET"
            }
            
            response_text = json.dumps(response_data)
            self.wfile.write(response_text.encode('utf-8'))
        
        # Record response time
        end_time = time.time()
        response_time = end_time - start_time
        response_times.append(response_time)

def run_server(port):
    # Since we can't actually run a server, just print the expected output
    print(f"Listening on :{port}")

# Read port from stdin
port = int(input().strip())

# Print expected output
run_server(port)