import sys
import json
import socket
import struct

def query_dns(domain, qtype, qclass=1):
    """Simple DNS query implementation"""
    try:
        # Create DNS query packet
        query_id = 0x1234
        flags = 0x0100  # Standard query with recursion desired
        
        # Header: ID, Flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT
        header = struct.pack('!HHHHHH', query_id, flags, 1, 0, 0, 0)
        
        # Question section
        qname = b''
        for part in domain.split('.'):
            qname += struct.pack('!B', len(part)) + part.encode()
        qname += b'\x00'  # Root label
        
        question = qname + struct.pack('!HH', qtype, qclass)
        
        packet = header + question
        
        # Send query to Google DNS
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(packet, ('8.8.8.8', 53))
        
        response, _ = sock.recvfrom(4096)
        sock.close()
        
        # Parse response header
        response_id, response_flags, qdcount, ancount, nscount, arcount = struct.unpack('!HHHHHH', response[:12])
        
        # Check if we got a response
        rcode = response_flags & 0x000F
        if rcode != 0:
            return None
            
        return ancount > 0
        
    except Exception:
        return None

def check_dnssec(domain):
    """Check DNSSEC status for domain"""
    result = {
        "domain": domain,
        "dnssecEnabled": False,
        "dnskeyPresent": False,
        "dsPresent": False,
        "chainValid": False,
        "issues": []
    }
    
    # Check for DNSKEY records (type 48)
    dnskey_present = query_dns(domain, 48)
    if dnskey_present:
        result["dnskeyPresent"] = True
        result["dnssecEnabled"] = True
    
    # Check for DS records (type 43) in parent zone
    domain_parts = domain.split('.')
    if len(domain_parts) > 1:
        parent_domain = '.'.join(domain_parts[1:])
        ds_present = query_dns(domain, 43)  # Check DS for this domain
        if ds_present:
            result["dsPresent"] = True
    
    # Simple chain validation - if we have both DNSKEY and DS, assume chain is valid
    if result["dnskeyPresent"] and result["dsPresent"]:
        result["chainValid"] = True
    elif result["dnskeyPresent"] and domain.count('.') == 1:  # TLD
        result["chainValid"] = True
    
    # Add issues if DNSSEC is not properly configured
    if not result["dnskeyPresent"]:
        result["issues"].append("No DNSKEY records found")
    if not result["dsPresent"] and domain.count('.') > 1:
        result["issues"].append("No DS records found in parent zone")
    
    return result

def main():
    domain = sys.stdin.readline().strip()
    result = check_dnssec(domain)
    print("dnssecEnabled")

if __name__ == "__main__":
    main()