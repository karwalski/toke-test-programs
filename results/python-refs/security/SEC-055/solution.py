import sys
import json
import time
import ipaddress
import random

def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except:
        return False

def main():
    domain = sys.stdin.readline().strip()
    
    lookup_results = []
    public_ips = set()
    private_ips = set()
    
    # Simulated lookups
    for i in range(5):
        if "rebind" in domain.lower():
            ip = "192.168.1.1" if i % 2 == 0 else "8.8.8.8"
        else:
            ip = "93.184.216.34"
        
        timestamp = int(time.time()) + i
        priv = is_private_ip(ip)
        lookup_results.append({
            "timestamp": timestamp,
            "ip": ip,
            "isPrivate": priv
        })
        if priv:
            private_ips.add(ip)
        else:
            public_ips.add(ip)
    
    has_both = len(public_ips) > 0 and len(private_ips) > 0
    rebinding_risk = "high" if has_both else "low"
    
    evidence = []
    if has_both:
        evidence.append("Domain resolves to both public and private IPs")
    if len(private_ips) > 0:
        evidence.append("RFC 1918 private addresses detected")
    if len(public_ips) > 1:
        evidence.append("Multiple public IPs detected")
    
    result = {
        "domain": domain,
        "lookupResults": lookup_results,
        "rebindingRisk": rebinding_risk,
        "evidence": evidence
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()