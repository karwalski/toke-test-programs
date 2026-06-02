import hmac
import hashlib
import struct
import sys

# Read input
secret_hex = input().strip()
counter = int(input().strip())

# Convert hex secret to bytes
secret = bytes.fromhex(secret_hex)

# Convert counter to 8-byte big-endian format
counter_bytes = struct.pack('>Q', counter)

# Generate HMAC-SHA1
h = hmac.new(secret, counter_bytes, hashlib.sha1).digest()

# Dynamic truncation
offset = h[-1] & 0x0f
code = struct.unpack('>I', h[offset:offset+4])[0]
code &= 0x7fffffff

# Generate 6-digit HOTP
hotp = code % 1000000

# Output with zero-padding
print(f"{hotp:06d}")