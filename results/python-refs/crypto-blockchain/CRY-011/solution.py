import hashlib
import sys

# Read hex string from stdin
hex_input = input().strip()

# Convert hex string to bytes
input_bytes = bytes.fromhex(hex_input)

# First SHA-256 hash
first_hash = hashlib.sha256(input_bytes).digest()

# Second SHA-256 hash (hash the hash)
second_hash = hashlib.sha256(first_hash).digest()

# Convert to lowercase hex and output
print(second_hash.hex())