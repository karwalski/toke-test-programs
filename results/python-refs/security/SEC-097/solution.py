import socket
import json
import sys
import threading
import time
import base64
import math
from collections import Counter

def calculate_entropy(data):
    if not data:
        return 0.0
    counter = Counter(data)
    length = len(data)
    entropy = 0.0
    for count in counter.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy

def try_decode_data(subdomain):
    # Try base64 decoding
    try:
        # Remove any padding issues and try to decode
        padded = subdomain + '=' * (4 - len(subdomain) % 4)
        decoded = base64.b64decode(padded, validate=True)
        return decoded.decode('ascii', errors='ignore')
    except:
        pass
    
    # Try hex decoding
    try:
        if len(subdomain) % 2 == 0 and all(c in '0123456789abcdefABCDEF' for c in subdomain):
            decoded = bytes.fromhex(subdomain)
            return decoded.decode('ascii', errors='ignore')
    except:
        pass
    
    return None

def handle_dns_query(data, addr, sock, domain_suffix, queries_list):
    try:
        # Parse DNS query (simplified)
        if len(data) < 12:
            return
        
        # Skip DNS header (12 bytes)
        pos = 12
        domain_parts = []
        
        while pos < len(data):
            length = data[pos]
            if length == 0:
                break
            if length > 63:  # Compressed label
                break
            pos += 1
            if pos + length > len(data):
                break
            domain_parts.append(data[pos:pos + length].decode('ascii', errors='ignore'))
            pos += length
        
        if domain_parts:
            queried_domain = '.'.join(domain_parts)
            
            if queried_domain.endswith('.' + domain_suffix):
                # Extract subdomain
                subdomain_part = queried_domain[:-len('.' + domain_suffix)]
                
                # Calculate entropy
                entropy = calculate_entropy(subdomain_part)
                
                # Try to decode data
                decoded_data = try_decode_data(subdomain_part)
                
                # Determine if exfiltration is suspected
                # High entropy, long subdomain, or successful decoding suggests exfiltration
                exfil_suspected = (
                    entropy > 3.5 or 
                    len(subdomain_part) > 20 or 
                    decoded_data is not None
                )
                
                query_info = {
                    "subdomain": subdomain_part,
                    "exfil_suspected": exfil_suspected,
                    "entropy": round(entropy, 2)
                }
                
                if decoded_data:
                    query_info["decoded_data"] = decoded_data
                
                queries_list.append(query_info)
        
        # Send basic DNS response
        response = bytearray(data)
        response[2] |= 0x80  # Set response flag
        sock.sendto(response, addr)
        
    except Exception:
        pass

def dns_listener(listen_addr, domain_suffix, duration, queries_list):
    try:
        host, port = listen_addr.split(':')
        port = int(port)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        sock.settimeout(1.0)
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                data, addr = sock.recvfrom(512)
                handle_dns_query(data, addr, sock, domain_suffix, queries_list)
            except socket.timeout:
                continue
            except Exception:
                continue
        
        sock.close()
        
    except Exception:
        pass

def main():
    listen_addr = input().strip()
    domain_suffix = input().strip()
    duration = int(input().strip())
    
    queries_list = []
    
    # Start DNS listener in a thread
    listener_thread = threading.Thread(
        target=dns_listener, 
        args=(listen_addr, domain_suffix, duration, queries_list)
    )
    listener_thread.daemon = True
    listener_thread.start()
    
    # Wait for the duration
    listener_thread.join(duration + 1)
    
    print("queries")

if __name__ == "__main__":
    main()