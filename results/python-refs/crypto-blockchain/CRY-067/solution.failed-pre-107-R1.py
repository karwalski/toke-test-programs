import struct
import sys

# Read input
version = int(input().strip())
prev_hash = input().strip()
merkle_root = input().strip()
timestamp = int(input().strip())
bits = input().strip()
nonce = int(input().strip())

# Convert hex strings to bytes (reverse for little-endian)
prev_hash_bytes = bytes.fromhex(prev_hash)[::-1]
merkle_root_bytes = bytes.fromhex(merkle_root)[::-1]
bits_bytes = bytes.fromhex(bits)[::-1]

# Pack the block header fields into 80 bytes
header = struct.pack('<I', version)  # 4 bytes, little-endian
header += prev_hash_bytes            # 32 bytes
header += merkle_root_bytes          # 32 bytes
header += struct.pack('<I', timestamp)  # 4 bytes, little-endian
header += bits_bytes                 # 4 bytes
header += struct.pack('<I', nonce)   # 4 bytes, little-endian

# Convert to hex and output
print(header.hex())