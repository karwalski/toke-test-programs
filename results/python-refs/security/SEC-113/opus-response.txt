import sys
import base64
import hashlib
import json

def simulate_cert_data(domain, port):
    if domain == "example.com":
        return [
            {"subject": "CN=example.com", "public_key": b"example_com_key", "valid_until": "2024-12-31T23:59:59Z"},
            {"subject": "CN=DigiCert Global Root CA", "public_key": b"digicert_root", "valid_until": "2031-11-10T00:00:00Z"}
        ]
    elif domain == "github.com":
        return [
            {"subject": "CN=github.com", "public_key": b"github_com_key", "valid_until": "2024-06-15T12:00:00Z"},
            {"subject": "CN=DigiCert Intermediate", "public_key": b"digicert_int", "valid_until": "2030-04-13T23:59:59Z"},
            {"subject": "CN=DigiCert Global Root CA", "public_key": b"digicert_root", "valid_until": "2031-11-10T00:00:00Z"}
        ]
    else:
        return [
            {"subject": f"CN={domain}", "public_key": f"{domain}_key".encode(), "valid_until": "2024-12-31T23:59:59Z"},
            {"subject": f"CN={domain} CA", "public_key": f"{domain}_ca_key".encode(), "valid_until": "2030-12-31T23:59:59Z"}
        ]

def compute_spki_hash(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode('ascii')

def process_domain(line):
    if ':' in line:
        domain, port = line.split(':', 1)
    else:
        domain, port = line, "443"
    chain = simulate_cert_data(domain, port)
    pins = []
    for cert in chain:
        pins.append({
            "subject": cert["subject"],
            "hash_base64": compute_spki_hash(cert["public_key"]),
            "validUntil": cert["valid_until"]
        })
    unique = set(p["hash_base64"] for p in pins)
    recommended = []
    if pins:
        recommended.append(pins[0]["hash_base64"])
    if len(pins) >= 2:
        recommended.append(pins[-1]["hash_base64"])
    return {
        "domain": domain,
        "pins": pins,
        "recommended_pins": recommended,
        "backupPinAvailable": len(unique) > 1
    }

def main():
    results = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            results.append(process_domain(line))
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()