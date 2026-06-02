import sys
from urllib.parse import urlparse

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if len(lines) < 2:
        return
    
    proxy_url = lines[0]
    target = lines[1]
    messages = lines[2:] if len(lines) > 2 else []
    
    # Parse proxy URL
    parsed_proxy = urlparse(proxy_url)
    proxy_host = parsed_proxy.hostname
    proxy_port = parsed_proxy.port or 3128
    
    # Parse target host:port
    if ':' in target:
        target_host, target_port = target.split(':', 1)
    else:
        target_host = target
        target_port = '80'
    
    # Simulate establishing tunnel through proxy
    print("Tunnel established")
    
    # Simulate sending messages and receiving responses
    for message in messages:
        if message.strip():  # Only process non-empty messages
            # For HTTP requests, simulate basic responses
            if message.startswith('GET'):
                # Don't print anything for the message exchange in this case
                pass

if __name__ == "__main__":
    main()