import sys
import hashlib

# Read hex-encoded public key from stdin
hex_pubkey = sys.stdin.read().strip()

# Convert hex to bytes
pubkey_bytes = bytes.fromhex(hex_pubkey)

# Calculate SHA256 hash
sha256_hash = hashlib.sha256(pubkey_bytes).digest()

# Calculate RIPEMD160 hash of the SHA256 result
ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

# Convert to lowercase hex and output
print(ripemd160_hash.hex())