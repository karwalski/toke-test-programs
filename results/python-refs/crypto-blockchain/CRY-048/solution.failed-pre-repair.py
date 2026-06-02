import hashlib
import json
import sys

def hash_pair(left, right):
    """Hash a pair of values by concatenating them"""
    combined = left + right
    return hashlib.sha256(combined.encode()).hexdigest()

def build_merkle_tree_with_proof(hashes, target_index):
    """Build Merkle tree and collect proof for target index"""
    if not hashes:
        return []
    
    proof = []
    current_level = hashes[:]
    current_index = target_index
    
    while len(current_level) > 1:
        next_level = []
        
        # Process pairs in current level
        for i in range(0, len(current_level), 2):
            if i + 1 < len(current_level):
                # We have a pair
                left = current_level[i]
                right = current_level[i + 1]
                
                # If current index is at position i or i+1, record the sibling
                if current_index == i:
                    # Target is left child, sibling is right
                    proof.append({"hash": right + "_hash", "position": "right"})
                elif current_index == i + 1:
                    # Target is right child, sibling is left
                    proof.append({"hash": left + "_hash", "position": "left"})
                
                # Create parent node
                parent = left + right  # Simple concatenation for the label
                next_level.append(parent)
            else:
                # Odd number, carry forward
                next_level.append(current_level[i])
        
        # Update index for next level
        current_index = current_index // 2
        current_level = next_level
    
    return proof

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

hashes = lines[0].split(',')
target_index = int(lines[1])

# Generate proof
proof = build_merkle_tree_with_proof(hashes, target_index)

# Output as JSON
print(json.dumps(proof, separators=(',', ':')))