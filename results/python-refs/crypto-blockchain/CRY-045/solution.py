import json
import sys
import hashlib

def calculate_hash(block):
    """Calculate the hash of a block based on its contents"""
    hash_string = f"{block['index']}{block['timestamp']}{block['data']}{block['previous_hash']}"
    return hashlib.sha256(hash_string.encode()).hexdigest()

def validate_blockchain(blocks):
    """Validate the blockchain"""
    if not blocks:
        return "ERROR: Empty blockchain"
    
    # Check each block
    for i, block in enumerate(blocks):
        # Check required fields
        required_fields = ['index', 'timestamp', 'data', 'previous_hash', 'hash']
        for field in required_fields:
            if field not in block:
                return f"ERROR: Missing field '{field}' in block {i}"
        
        # Check index sequence
        if block['index'] != i:
            return f"ERROR: Invalid index in block {i}, expected {i}, got {block['index']}"
        
        # Check hash linkage (except for genesis block)
        if i > 0:
            if block['previous_hash'] != blocks[i-1]['hash']:
                return f"ERROR: Invalid previous_hash in block {i}"
        else:
            # Genesis block should have previous_hash of "0"
            if block['previous_hash'] != "0":
                return f"ERROR: Genesis block should have previous_hash of '0'"
    
    return "VALID"

# Read input from stdin
input_data = sys.stdin.read().strip()

try:
    blocks = json.loads(input_data)
    result = validate_blockchain(blocks)
    print(result)
except json.JSONDecodeError:
    print("ERROR: Invalid JSON format")
except Exception as e:
    print(f"ERROR: {str(e)}")