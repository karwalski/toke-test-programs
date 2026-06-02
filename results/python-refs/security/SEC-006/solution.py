import sys
import json
import ipaddress

def classify_ip(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str.strip())
    except ValueError:
        return {"ip": ip_str.strip(), "reputation": "malicious", "reason": "invalid IP address"}
    
    # Known Tor exit node prefixes (sample list)
    tor_prefixes = [
        "199.87.154.",
        "185.220.",
        "45.61.186.",
        "91.218.203."
    ]
    
    # Check for Tor exit nodes
    for prefix in tor_prefixes:
        if ip_str.startswith(prefix):
            return {"ip": ip_str.strip(), "reputation": "suspicious", "reason": "known Tor exit node"}
    
    # Check if private (RFC 1918)
    if ip.is_private:
        return {"ip": ip_str.strip(), "reputation": "private", "reason": "RFC 1918 private address"}
    
    # Check if loopback
    if ip.is_loopback:
        return {"ip": ip_str.strip(), "reputation": "private", "reason": "loopback address"}
    
    # Check if link-local (APIPA)
    if ip.is_link_local:
        return {"ip": ip_str.strip(), "reputation": "reserved", "reason": "APIPA/link-local address"}
    
    # Check if reserved/documentation ranges
    if ip.is_reserved:
        return {"ip": ip_str.strip(), "reputation": "reserved", "reason": "reserved address range"}
    
    # Check documentation ranges manually (since is_reserved might not catch all)
    if isinstance(ip, ipaddress.IPv4Address):
        # TEST-NET ranges
        if ip in ipaddress.IPv4Network('192.0.2.0/24') or \
           ip in ipaddress.IPv4Network('198.51.100.0/24') or \
           ip in ipaddress.IPv4Network('203.0.113.0/24'):
            return {"ip": ip_str.strip(), "reputation": "reserved", "reason": "documentation range"}
    
    # Default to clean
    return {"ip": ip_str.strip(), "reputation": "clean", "reason": "no threats detected"}

def main():
    for line in sys.stdin:
        line = line.strip()
        if line:
            result = classify_ip(line)
            print(result["reputation"])
            break

if __name__ == "__main__":
    main()