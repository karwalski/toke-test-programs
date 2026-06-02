import sys, hashlib, base64

def main():
    data = sys.stdin.read().splitlines()
    version = int(data[0].strip())
    key_a = data[1].strip()
    key_b = data[2].strip()
    keys = sorted([key_a, key_b])
    a_bytes = bytes.fromhex(keys[0])
    b_bytes = bytes.fromhex(keys[1])
    combined = a_bytes + b_bytes
    fp = hashlib.sha256(combined).digest()
    fp_hex = fp.hex()
    payload = bytes([version]) + fp
    qr = base64.b64encode(payload).decode('ascii')
    n = int(fp_hex, 16)
    digits = str(n).zfill(78)[:30]
    groups = ' '.join(digits[i:i+5] for i in range(0, 30, 5))
    print(f"qr_payload: {qr}")
    print(f"numeric_code: {groups}")
    print(f"version: {version}")
    print(f"fingerprint: {fp_hex}")

main()
