import sys
import socket
import json
import time
import ipaddress

def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except:
        return False

def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def main():
    domain = sys.stdin.readline().strip()
    
    lookup_results = []
    public_ips = set()
    private_ips = set()
    
    # Perform multiple lookups to detect rebinding
    for _ in range(5):
        ip = resolve_domain(domain)
        if ip:
            timestamp = int(time.time())
            is_private = is_private_ip(ip)
            
            lookup_results.append({
                "timestamp": timestamp,
                "ip": ip,
                "isPrivate": is_private
            })
            
            if is_private:
                private_ips.add(ip)
            else:
                public_ips.add(ip)
        
        time.sleep(0.1)
    
    # Determine rebinding risk
    has_both = len(public_ips) > 0 and len(private_ips) > 0
    rebinding_risk = "high" if has_both else "low"
    
    evidence = []
    if has_both:
        evidence.append("Domain resolves to both public and private IPs")
    if len(public_ips) > 1:
        evidence.append("Multiple public IPs detected")
    if len(private_ips) > 1:
        evidence.append("Multiple private IPs detected")
    
    result = {
        "domain": domain,
        "lookupResults": lookup_results,
        "rebindingRisk": rebinding_risk,
        "evidence": evidence
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()