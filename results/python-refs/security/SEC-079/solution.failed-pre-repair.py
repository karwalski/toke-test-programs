import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

def query_crt_sh(domain):
    """Query crt.sh for certificates for the given domain"""
    url = f"https://crt.sh/?q={urllib.parse.quote(domain)}&output=json"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return json.loads(data)
    except Exception:
        return []

def parse_cert_data(cert_data, allowed_cas):
    """Parse certificate data and identify alerts"""
    alert_certs = []
    
    for cert in cert_data:
        issuer = cert.get('issuer_name', '')
        common_name = cert.get('common_name', '')
        not_before = cert.get('not_before', '')
        
        # Check if CA is allowed
        ca_allowed = False
        for allowed_ca in allowed_cas:
            if allowed_ca.lower() in issuer.lower():
                ca_allowed = True
                break
        
        if not ca_allowed:
            alert_certs.append({
                'issuer': issuer,
                'commonName': common_name,
                'notBefore': not_before,
                'reason': 'Unexpected CA'
            })
    
    return alert_certs

def main():
    # Read input
    domain = input().strip()
    allowed_cas_json = input().strip()
    allowed_cas = json.loads(allowed_cas_json)
    
    # Query crt.sh
    cert_data = query_crt_sh(domain)
    
    # Parse and analyze certificates
    alert_certs = parse_cert_data(cert_data, allowed_cas)
    
    # Create summary
    total_certs = len(cert_data)
    alert_count = len(alert_certs)
    
    if alert_count == 0:
        summary = "No alerts found"
    else:
        summary = f"{alert_count} certificate(s) with unexpected CAs found"
    
    # Output result
    result = {
        'domain': domain,
        'totalCerts': total_certs,
        'alertCerts': alert_certs,
        'summary': summary
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()