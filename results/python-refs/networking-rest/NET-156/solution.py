import sys
import urllib.request
import urllib.parse
import json
import hashlib
import hmac

def main():
    # Read input from stdin
    sse_url = input().strip()
    webhook_url = input().strip()
    secret = input().strip()
    
    print("Relaying")
    
    try:
        # Open SSE stream
        req = urllib.request.Request(sse_url)
        req.add_header('Accept', 'text/event-stream')
        req.add_header('Cache-Control', 'no-cache')
        
        with urllib.request.urlopen(req) as response:
            buffer = ""
            event_data = {}
            
            for line in response:
                line = line.decode('utf-8').rstrip('\n\r')
                
                if line == "":
                    # Empty line indicates end of event
                    if event_data:
                        relay_event(webhook_url, secret, event_data)
                        event_data = {}
                    continue
                
                if line.startswith("data: "):
                    data = line[6:]  # Remove "data: " prefix
                    if 'data' in event_data:
                        event_data['data'] += '\n' + data
                    else:
                        event_data['data'] = data
                elif line.startswith("event: "):
                    event_data['event'] = line[7:]  # Remove "event: " prefix
                elif line.startswith("id: "):
                    event_data['id'] = line[4:]  # Remove "id: " prefix
                elif line.startswith("retry: "):
                    event_data['retry'] = line[7:]  # Remove "retry: " prefix
                    
    except Exception as e:
        pass

def relay_event(webhook_url, secret, event_data):
    try:
        # Prepare payload
        payload = json.dumps(event_data).encode('utf-8')
        
        # Create HMAC signature
        signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Create request
        req = urllib.request.Request(
            webhook_url,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'X-Signature-256': f'sha256={signature}'
            },
            method='POST'
        )
        
        # Send request
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            print(f"Event relayed: {status}")
            
    except Exception as e:
        print(f"Event relayed: error")

if __name__ == "__main__":
    main()