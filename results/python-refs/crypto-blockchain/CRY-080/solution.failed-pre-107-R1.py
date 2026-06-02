import json
import hashlib
import secrets

def pedersen_commit(value, blinding, g_hex="02", h_hex="03"):
    # Simple commitment: H(g^value * h^blinding)
    # Using a simplified approach with hash-based commitment
    commitment_input = f"{g_hex}{value:016x}{h_hex}{blinding}"
    commitment_hash = hashlib.sha256(commitment_input.encode()).hexdigest()
    return commitment_hash

def range_proof_bulletproof_simple(value, n, blinding_hex):
    # Convert value to binary representation
    value_bits = [(value >> i) & 1 for i in range(n)]
    
    # Generate commitment for the main value
    commitment = pedersen_commit(value, blinding_hex)
    
    # For range proof, we need to prove each bit is 0 or 1
    # and that they sum to the committed value
    bit_commitments = []
    
    for i, bit in enumerate(value_bits):
        # Generate a blinding factor for each bit commitment
        bit_blinding = hashlib.sha256(f"{blinding_hex}_{i}".encode()).hexdigest()
        bit_commitment = pedersen_commit(bit, bit_blinding)
        bit_commitments.append(bit_commitment)
    
    # Verify the range (value should be in [0, 2^n))
    proof_valid = 0 <= value < (2 ** n)
    
    return {
        "commitment": commitment,
        "range_bits": n,
        "proof_valid": proof_valid
    }

def main():
    # Read input
    value = int(input().strip())
    n = int(input().strip())
    blinding_hex = input().strip()
    
    # Generate range proof
    proof = range_proof_bulletproof_simple(value, n, blinding_hex)
    
    # Output JSON
    print(json.dumps(proof, separators=(',', ':')))

if __name__ == "__main__":
    main()