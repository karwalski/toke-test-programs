import sys, json, base64

def xor_encrypt(key_bytes, plaintext_bytes):
    out = bytearray()
    for i, b in enumerate(plaintext_bytes):
        out.append(b ^ key_bytes[i % len(key_bytes)])
    return bytes(out)

def main():
    data = sys.stdin.read().split('\n')
    ring = json.loads(data[0])
    active = int(data[1].strip())
    op = data[2].strip()
    payload = data[3]
    keys = {entry['version']: bytes.fromhex(entry['key']) for entry in ring}
    if op == 'encrypt':
        if active not in keys:
            print(f'Error: unknown key version {active}')
            return
        key = keys[active]
        ct = xor_encrypt(key, payload.encode('utf-8'))
        b64 = base64.b64encode(ct).decode('ascii')
        print(f'v{active}:{b64}')
    elif op == 'decrypt':
        if ':' not in payload:
            print('Error: invalid ciphertext format')
            return
        prefix, b64 = payload.split(':', 1)
        if not prefix.startswith('v'):
            print('Error: invalid version prefix')
            return
        try:
            version = int(prefix[1:])
        except ValueError:
            print('Error: invalid version number')
            return
        if version not in keys:
            print(f'Error: unknown key version {version}')
            return
        key = keys[version]
        try:
            ct = base64.b64decode(b64)
        except Exception:
            print('Error: invalid base64')
            return
        pt = xor_encrypt(key, ct).decode('utf-8', errors='replace')
        print(f'{pt} (decrypted with key v{version})')
    else:
        print(f'Error: unknown operation {op}')

main()
