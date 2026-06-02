import hashlib
import sys

# Read input
block_data = input().strip()
difficulty = int(input().strip())

# Find nonce that produces hash with required leading zeros
nonce = 0
target_prefix = '0' * difficulty

while True:
    # Create the data to hash (block_data + nonce)
    data_to_hash = block_data + str(nonce)
    
    # Calculate SHA-256 hash
    hash_object = hashlib.sha256(data_to_hash.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    
    # Check if hash has required leading zeros
    if hash_hex.startswith(target_prefix):
        # Found valid nonce
        print(nonce)
        print(hash_hex)
        break
    
    nonce += 1