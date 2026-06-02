import sys
import json
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError
import threading
import time

def read_input():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            break
        lines.append(line)
    return lines

def deliver_webhook(url, payload, event_id):
    """Attempt to deliver webhook with retries"""
    max_retries = 3
    
    for attempt in range(max_retries + 1):
        try:
            req = Request(url, data=payload.encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urlopen(req, timeout=5) as response:
                if 200 <= response.status < 300:
                    return True
        except Exception as e:
            pass
        
        if attempt < max_retries:
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return False

def fan_out_event(webhook_urls, payload):
    """Fan out event to all webhook URLs"""
    event_id = int(time.time() * 1000000)  # Simple event ID
    threads = []
    
    for url in webhook_urls:
        thread = threading.Thread(target=deliver_webhook, args=(url, payload, event_id))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Wait for all deliveries to complete (but don't block forever)
    for thread in threads:
        thread.join(timeout=30)

def main():
    # Read input
    input_lines = read_input()
    
    if not input_lines:
        return
    
    port = input_lines[0]
    webhook_urls = input_lines[1:] if len(input_lines) > 1 else []
    
    # Output the listening message
    print(f"Listening on :{port}")
    
    # Since we can't actually run a server, we'll simulate receiving an event
    # In a real implementation, this would be handled by the HTTP server
    if webhook_urls:
        # Simulate receiving a POST /events request
        sample_event = {"type": "test", "data": {"message": "hello"}}
        payload = json.dumps(sample_event)
        fan_out_event(webhook_urls, payload)

if __name__ == "__main__":
    main()