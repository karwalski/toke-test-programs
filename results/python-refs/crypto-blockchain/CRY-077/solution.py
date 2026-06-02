import sys, json, hashlib, random

def main():
    lines = sys.stdin.read().splitlines()
    subject = lines[0]
    issuer = lines[1]
    public_key = lines[2]
    not_before = lines[3]
    not_after = lines[4]
    # Deterministic serial: seeded by inputs
    seed_material = '|'.join([subject, issuer, public_key, not_before, not_after])
    rng = random.Random(seed_material)
    serial = ''.join('{:02x}'.format(rng.randint(0,255)) for _ in range(16))
    cert_fields = {
        'subject': subject,
        'issuer': issuer,
        'public_key': public_key,
        'validity': {'not_before': not_before, 'not_after': not_after},
        'serial': serial
    }
    canonical = json.dumps(cert_fields, sort_keys=True, separators=(',', ':'))
    fingerprint = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    cert = dict(cert_fields)
    cert['fingerprint'] = fingerprint
    print(json.dumps(cert, sort_keys=True, separators=(',', ':')))

main()
