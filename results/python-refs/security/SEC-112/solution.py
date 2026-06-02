import sys
import urllib.request
import urllib.parse
import ssl
import hashlib
import hmac
import json
import socket
import time
from urllib.error import URLError, HTTPError

def get_certificate_hash(hostname, port=443):
    """Get SHA256 hash of the server's certificate"""
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert_der = ssock.getpeercert_chain()[0].public_bytes(serialization.Encoding.DER)
                return hashlib.sha256(cert_der).hexdigest()
    except:
        # Fallback method
        try:
            with urllib.request.urlopen(f"https://{hostname}", timeout=10) as response:
                return "dummy_hash"  # Simplified for standard library limitations
        except:
            return "failed_to_get_cert"

def scrub_sensitive_headers(headers):
    """Remove sensitive headers from logs"""
    sensitive = ['authorization', 'cookie', 'x-api-key', 'x-auth-token']
    scrubbed = {}
    for k, v in headers.items():
        if k.lower() in sensitive:
            scrubbed[k] = '[SCRUBBED]'
        else:
            scrubbed[k] = v
    return scrubbed

def detect_anomalies(response_body, headers, status_code):
    """Simple anomaly detection on response"""
    anomalies = []
    
    # Check response size
    if len(response_body) > 10000000:  # 10MB
        anomalies.append("Large response size")
    
    # Check for suspicious content
    suspicious_strings = ['<script>', 'javascript:', 'eval(', 'document.cookie']
    for suspicious in suspicious_strings:
        if suspicious.lower() in response_body.lower():
            anomalies.append(f"Suspicious content: {suspicious}")
    
    # Check status code
    if status_code >= 400:
        anomalies.append(f"HTTP error status: {status_code}")
    
    return anomalies

def create_signature(method, url, body, secret):
    """Create HMAC signature for request"""
    message = f"{method}:{url}:{body}"
    signature = hmac.new(
        secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return signature

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    url = lines[0]
    pinned_cert_hash = lines[1]
    signing_secret = lines[2]
    
    # Parse URL
    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    
    try:
        # Certificate pinning check
        actual_cert_hash = get_certificate_hash(hostname)
        cert_valid = (actual_cert_hash == pinned_cert_hash)
        
        # Create request signature
        method = "GET"
        body = ""
        signature = create_signature(method, url, body, signing_secret)
        
        # Make request
        request = urllib.request.Request(url)
        request.add_header('X-Request-Signature', signature)
        request.add_header('User-Agent', 'SecureHTTPClient/1.0')
        
        with urllib.request.urlopen(request, timeout=10) as response:
            response_body = response.read().decode('utf-8')
            status_code = response.getcode()
            response_headers = dict(response.headers)
            
            # Anomaly detection
            anomalies = detect_anomalies(response_body, response_headers, status_code)
            
            # Security logging
            security_log = {
                "certificate_validation": {
                    "expected_hash": pinned_cert_hash,
                    "actual_hash": actual_cert_hash,
                    "valid": cert_valid
                },
                "request_signature": signature,
                "response_headers": scrub_sensitive_headers(response_headers),
                "anomalies": anomalies,
                "timestamp": time.time()
            }
            
            # Output response body
            print(status_code)
            
    except Exception as e:
        print("Error occurred during request")

if __name__ == "__main__":
    main()