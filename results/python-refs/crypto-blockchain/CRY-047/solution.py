import hashlib
import sys

def compute_merkle_root(hashes):
    if len(hashes) == 1:
        return hashes[0]
    
    next_level = []
    
    # Process pairs
    for i in range(0, len(hashes), 2):
        if i + 1 < len(hashes):
            # Pair exists
            combined = hashes[i] + hashes[i + 1]
        else:
            # Odd number, duplicate the last hash
            combined = hashes[i] + hashes[i]
        
        # Hash the combined string
        hash_result = hashlib.sha256(combined.encode()).hexdigest()
        next_level.append(hash_result)
    
    return compute_merkle_root(next_level)

# Read input
hashes = []
for line in sys.stdin:
    hash_value = line.strip()
    if hash_value:
        hashes.append(hash_value)

# Compute and output Merkle root
root = compute_merkle_root(hashes)
print(root)