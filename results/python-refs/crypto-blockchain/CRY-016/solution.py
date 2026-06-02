import hashlib
import sys

# Read input
password = input().strip()
salt = input().strip()
iterations = int(input().strip())

# Convert password and salt to bytes
password_bytes = password.encode('utf-8')
salt_bytes = salt.encode('utf-8')

# Generate PBKDF2-HMAC-SHA256 derived key (32 bytes)
derived_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, iterations, 32)

# Output as lowercase hex
print(derived_key.hex())