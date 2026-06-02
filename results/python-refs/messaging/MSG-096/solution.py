import sys, json, hashlib, base64

def main():
    lines = sys.stdin.read().splitlines()
    filename = lines[0]
    size = int(lines[1])
    mime = lines[2]
    content_hash = lines[3]
    key_hex = lines[4]
    key = bytes.fromhex(key_hex)
    plain = json.dumps({"filename": filename, "mime": mime}, sort_keys=True, separators=(',', ':')).encode('utf-8')
    out = bytes(plain[i] ^ key[i % len(key)] for i in range(len(plain)))
    enc_b64 = base64.b64encode(out).decode('ascii')
    key_hash = hashlib.sha256(key).hexdigest()
    result = {"encrypted_metadata": enc_b64, "content_hash": content_hash, "size": size, "key_hash": key_hash}
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))

main()
