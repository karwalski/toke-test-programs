import base64
import hmac
import hashlib
import struct
import sys

# Read input
secret_b32 = input().strip()
timestamp = int(input().strip())

# Decode base32 secret
secret = base64.b32decode(secret_b32)

# Calculate time counter (30-second intervals)
time_counter = timestamp // 30

# Convert counter to 8-byte big-endian
counter_bytes = struct.pack('>Q', time_counter)

# Generate HMAC-SHA1
hmac_digest = hmac.new(secret, counter_bytes, hashlib.sha1).digest()

# Dynamic truncation
offset = hmac_digest[-1] & 0x0f
code = struct.unpack('>I', hmac_digest[offset:offset+4])[0]
code &= 0x7fffffff

# Generate 6-digit code
totp = code % 1000000

# Output zero-padded 6-digit code
print(f"{totp:06d}")