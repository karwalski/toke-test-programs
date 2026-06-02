import sys
import base64
import hashlib

def simulate_cert_data(domain, port):
    """Simulate certificate data for known domains"""
    
    # Simulated certificate data for example.com
    if domain == "example.com" and port == "443":
        return [
            {
                "subject": "CN=example.com",
                "public_key": b"example_com_primary_key_data",
                "valid_until": "2024-12-31T23:59:59Z"
            },
            {
                "subject": "CN=DigiCert Global Root CA",
                "public_key": b"digicert_root_ca_key_data", 
                "valid_until": "2031-11-10T00:00:00Z"
            }
        ]
    
    # Simulated certificate data for github.com
    elif domain == "github.com" and port == "443":
        return [
            {
                "subject": "CN=github.com",
                "public_key": b"github_com_primary_key_data",
                "valid_until": "2024-06-15T12:00:00Z"
            },
            {
                "subject": "CN=DigiCert TLS Hybrid ECC SHA384 2020 CA1",
                "public_key": b"digicert_intermediate_ca_key_data",
                "valid_until": "2030-04-13T23:59:59Z"
            },
            {
                "subject": "CN=DigiCert Global Root CA", 
                "public_key": b"digicert_root_ca_key_data",
                "valid_until": "2031-11-10T00:00:00Z"
            }
        ]
    
    # Default fallback
    else:
        return [
            {
                "subject": f"CN={domain}",
                "public_key": f"{domain}_key_data".encode(),
                "valid_until": "2024-12-31T23:59:59Z"
            }
        ]

def compute_spki_hash(public_key_data):
    """Compute SHA256 hash of public key (HPKP-style)"""
    sha256_hash = hashlib.sha256(public_key_data).digest()
    return base64.b64encode(sha256_hash).decode('ascii')

def process_domain(domain_port):
    """Process a single domain:port pair"""
    if ':' in domain_port:
        domain, port = domain_port.split(':', 1)
    else:
        domain, port = domain_port, "443"
    
    # Get simulated certificate chain
    cert_chain = simulate_cert_data(domain, port)
    
    # Compute pins for each certificate in the chain
    pins = []
    for cert in cert_chain:
        hash_b64 = compute_spki_hash(cert["public_key"])
        pins.append({
            "subject": cert["subject"],
            "hash_base64": hash_b64,
            "validUntil": cert["valid_until"]
        })
    
    # Determine recommended pins (leaf + root CA)
    recommended_pins = []
    if len(pins) >= 1:
        recommended_pins.append(pins[0]["hash_base64"])  # Leaf cert
    if len(pins) >= 2:
        recommended_pins.append(pins[-1]["hash_base64"])  # Root CA
    
    # Check if backup pin is available (intermediate CA or additional certs)
    backup_pin_available = len(pins) > 2
    
    return {
        "domain": domain,
        "pins": pins,
        "recommended_pins": recommended_pins,
        "backupPinAvailable": backup_pin_available
    }

def main():
    """Main function to read from stdin and process domains"""
    results = []
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if line:
                result = process_domain(line)
                results.append(result)
    except EOFError:
        pass
    
    # Output results
    for result in results:
        print(f"Domain: {result['domain']}")
        print("Pins:")
        for pin in result['pins']:
            print(f"  Subject: {pin['subject']}")
            print(f"  Hash: {pin['hash_base64']}")
            print(f"  Valid Until: {pin['validUntil']}")
            print()
        
        print(f"Recommended Pins: {', '.join(result['recommended_pins'])}")
        print(f"Backup Pin Available: {result['backupPinAvailable']}")
        print()

if __name__ == "__main__":
    main()