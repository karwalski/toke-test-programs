import hashlib
import json
import sys

# Read input
index = int(input().strip())
timestamp = input().strip()
data = input().strip()
previous_hash = input().strip()

# Create block content for hashing
# The hash should be computed from the concatenation of all block fields
block_content = f"{index}{timestamp}{data}{previous_hash}"

# Compute SHA256 hash
hash_object = hashlib.sha256(block_content.encode('utf-8'))
computed_hash = hash_object.hexdigest()

# Create the block as a dictionary
block = {
    "index": index,
    "timestamp": timestamp,
    "data": data,
    "previous_hash": previous_hash,
    "hash": computed_hash
}

# Output as JSON (compact format, no spaces)
print(json.dumps(block, separators=(',', ':')))