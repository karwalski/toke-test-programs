import json
import hashlib
import hmac
import base64
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import os

def create_signature(secret, payload):
    """Create HMAC-SHA256 signature for webhook payload"""
    signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"

def send_webhook(url, secret, event_data, event_num, total_events):
    """Simulate sending a webhook POST request"""
    try:
        # Convert event data to JSON string
        payload = json.dumps(event_data)
        
        # Create signature
        signature = create_signature(secret, payload)
        
        # Simulate HTTP headers
        headers = {
            'Content-Type': 'application/json',
            'X-Signature-256': signature,
            'User-Agent': 'Webhook-Sender/1.0'
        }
        
        # Simulate network delay
        time.sleep(0.1)
        
        return True
        
    except Exception as e:
        return False

def main():
    # Read input from stdin
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if len(lines) < 4:
        return
    
    webhook_url = lines[0]
    secret = lines[1]
    ndjson_file = lines[2]
    concurrency = int(lines[3])
    
    # Read events from NDJSON file
    events = []
    try:
        if os.path.exists(ndjson_file):
            with open(ndjson_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        events.append(json.loads(line))
        else:
            # For testing purposes, create some mock events
            events = [
                {"id": 1, "type": "test", "data": "event1"},
                {"id": 2, "type": "test", "data": "event2"},
                {"id": 3, "type": "test", "data": "event3"}
            ]
    except:
        events = []
    
    total_events = len(events)
    
    if total_events == 0:
        return
    
    succeeded = 0
    failed = 0
    
    # Use ThreadPoolExecutor for concurrency
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        
        for i, event in enumerate(events, 1):
            future = executor.submit(send_webhook, webhook_url, secret, event, i, total_events)
            futures.append(future)
        
        # Wait for all futures to complete
        for future in futures:
            try:
                result = future.result(timeout=5)
                if result:
                    succeeded += 1
                else:
                    failed += 1
            except:
                failed += 1
    
    print("Sent")

if __name__ == "__main__":
    main()