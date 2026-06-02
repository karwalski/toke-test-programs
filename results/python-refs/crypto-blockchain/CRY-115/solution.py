import hashlib
import secrets

# Read input
password = input().strip()
iterations = int(input().strip())

# Generate random 16-byte salt
salt = secrets.token_bytes(16)

# Convert password to bytes
password_bytes = password.encode('utf-8')

# Derive key using PBKDF2-HMAC-SHA256
dk = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=32)

# Output salt as 32-char hex (16 bytes = 32 hex chars)
print(salt.hex())

# Output derived key as 64-char hex (32 bytes = 64 hex chars)
print(dk.hex())