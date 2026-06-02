import hashlib
import sys

mode = input().strip()

if mode == 'lines':
    for line in sys.stdin:
        line = line.rstrip('\n')
        hash_obj = hashlib.sha256(line.encode('utf-8'))
        hex_digest = hash_obj.hexdigest()
        print(f"{hex_digest}\t{line}")
elif mode == 'all':
    content = sys.stdin.read()
    hash_obj = hashlib.sha256(content.encode('utf-8'))
    hex_digest = hash_obj.hexdigest()
    print(hex_digest)