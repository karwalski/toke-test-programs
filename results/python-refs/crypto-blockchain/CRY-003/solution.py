import hashlib
import sys

# Read input from stdin
input_string = input().strip()

# Calculate MD5 hash
md5_hash = hashlib.md5(input_string.encode('utf-8')).hexdigest()

# Output the hash and warning
print(md5_hash)
print("WARNING: MD5 is cryptographically broken")