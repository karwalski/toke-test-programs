import sys
import hashlib
from datetime import datetime

# Read input data
data = input().strip()

# Get current timestamp in ISO 8601 format
timestamp = datetime.utcnow().isoformat() + 'Z'

# Concatenate data with timestamp
combined = data + timestamp

# Calculate SHA-256 hash
hash_object = hashlib.sha256(combined.encode('utf-8'))
hash_hex = hash_object.hexdigest()

# Output timestamp and hash
print(timestamp)
print(hash_hex)