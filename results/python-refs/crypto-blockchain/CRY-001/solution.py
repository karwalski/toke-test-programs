import hashlib
import sys

input_string = sys.stdin.readline().strip()
sha256_hash = hashlib.sha256(input_string.encode('utf-8')).hexdigest()
print(sha256_hash)