import sys

def main():
    data = sys.stdin.read().split('\n')
    lines = [l.strip() for l in data if l.strip() != '']
    version = int(lines[0])
    prev_hash = lines[1]
    merkle_root = lines[2]
    timestamp = int(lines[3])
    bits = lines[4]
    nonce = int(lines[5])
    out = b''
    out += version.to_bytes(4, 'little', signed=False)
    out += bytes.fromhex(prev_hash)[::-1]
    out += bytes.fromhex(merkle_root)[::-1]
    out += timestamp.to_bytes(4, 'little', signed=False)
    out += bytes.fromhex(bits)[::-1]
    out += nonce.to_bytes(4, 'little', signed=False)
    print(out.hex())

main()
