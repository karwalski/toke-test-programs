import json
import hashlib
import secrets

# Read input
subject = input().strip()
issuer = input().strip()
public_key = input().strip()
not_before = input().strip()
not_after = input().strip()

# Generate random serial number
serial = secrets.token_hex(16)

# Create certificate dictionary
certificate = {
    "subject": subject,
    "issuer": issuer,
    "public_key": public_key,
    "validity": {
        "not_before": not_before,
        "not_after": not_after
    },
    "serial": serial
}

# Create fingerprint by hashing all fields
# Convert certificate to a consistent string representation for hashing
cert_string = json.dumps(certificate, separators=(',', ':'), sort_keys=True)
fingerprint = hashlib.sha256(cert_string.encode()).hexdigest()

# Add fingerprint to certificate
certificate["fingerprint"] = fingerprint

# Output as JSON
print(json.dumps(certificate, separators=(',', ':')))