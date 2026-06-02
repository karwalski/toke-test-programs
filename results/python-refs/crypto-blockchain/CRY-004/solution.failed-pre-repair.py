import hmac
import hashlib
import sys

# Read key and message from stdin
key = input().strip()
message = input().strip()

# Convert key and message to bytes
key_bytes = key.encode('utf-8')
message_bytes = message.encode('utf-8')

# Calculate HMAC-SHA256
hmac_hash = hmac.new(key_bytes, message_bytes, hashlib.sha256)

# Output as lowercase hex
print(hmac_hash.hexdigest())