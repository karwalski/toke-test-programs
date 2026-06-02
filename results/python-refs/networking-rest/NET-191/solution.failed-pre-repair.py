import sys
import json
import urllib.parse
import hashlib
import hmac
import base64
from datetime import datetime

def read_har_file(har_path):
    """Read and parse HAR file to extract requests"""
    try:
        with open(har_path, 'r') as f:
            har_data = json.load(f)
        
        requests = []
        for entry in har_data.get('log', {}).get('entries', []):
            request = entry.get('request', {})
            requests.append({
                'method': request.get('method', 'GET'),
                'url': request.get('url', ''),
                'headers': {h['name']: h['value'] for h in request.get('headers', [])},
                'body': request.get('postData', {}).get('text', '')
            })
        
        return requests
    except:
        return []

def has_idempotency_key(request):
    """Check if request has idempotency key in headers"""
    headers = request.get('headers', {})
    for key in headers:
        if 'idempotency' in key.lower() or 'idempotent' in key.lower():
            return True
    return False

def has_timestamp_protection(request):
    """Check if request has timestamp-based protection"""
    headers = request.get('headers', {})
    body = request.get('body', '')
    
    # Check for timestamp in headers
    for key, value in headers.items():
        if 'timestamp' in key.lower() or 'date' in key.lower() or 'time' in key.lower():
            return True
    
    # Check for timestamp in body (JSON)
    try:
        if body:
            body_data = json.loads(body)
            for key in body_data:
                if 'timestamp' in key.lower() or 'time' in key.lower():
                    return True
    except:
        pass
    
    return False

def has_signature_protection(request):
    """Check if request has cryptographic signature"""
    headers = request.get('headers', {})
    
    for key in headers:
        key_lower = key.lower()
        if ('signature' in key_lower or 
            'authorization' in key_lower or 
            'x-signature' in key_lower or
            'x-hub-signature' in key_lower):
            return True
    
    return False

def analyze_replay_protection(request, mode):
    """Analyze if request is protected against replay attacks"""
    
    if mode == 'key':
        # Only check for idempotency keys
        return has_idempotency_key(request)
    
    elif mode == 'timestamp':
        # Check for timestamp-based protection
        return has_timestamp_protection(request) or has_signature_protection(request)
    
    elif mode == 'both':
        # Check for both idempotency keys AND timestamp protection
        return has_idempotency_key(request) and (has_timestamp_protection(request) or has_signature_protection(request))
    
    return False

def main():
    # Read input
    har_path = input().strip()
    mode = input().strip()
    
    # Read HAR file
    requests = read_har_file(har_path)
    
    # Analyze each request
    for request in requests:
        if analyze_replay_protection(request, mode):
            print('PROTECTED')
        else:
            print('VULNERABLE')

if __name__ == '__main__':
    main()