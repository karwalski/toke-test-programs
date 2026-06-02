import hashlib
import sys

for line in sys.stdin:
    line = line.rstrip('\n')
    md5_hash = hashlib.md5(line.encode('utf-8')).hexdigest()
    print(f"{md5_hash}\t{line}")