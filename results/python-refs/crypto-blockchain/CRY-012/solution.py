import hashlib
import sys

# Read input from stdin
text = input().strip()

# Create RIPEMD-160 hash
ripemd160 = hashlib.new('ripemd160')
ripemd160.update(text.encode('utf-8'))

# Output as lowercase hex
print(ripemd160.hexdigest())