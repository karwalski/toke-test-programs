import hmac
import hashlib

# Read the hex-encoded key and convert to bytes
key_hex = input().strip()
key = bytes.fromhex(key_hex)

# Read the message
message = input().strip()

# Compute HMAC-SHA256
hmac_digest = hmac.new(key, message.encode('utf-8'), hashlib.sha256).hexdigest()

# Output the hex-encoded digest
print(hmac_digest)