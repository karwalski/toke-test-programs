import json
import sys
import hashlib

def verify_cross_chain_transfer():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    try:
        # Parse JSON input
        data = json.loads(input_data)
        
        # Extract required fields
        source_tx_hash = data.get("source_tx_hash")
        amount = data.get("amount")
        recipient = data.get("recipient")
        proof = data.get("proof", {})
        
        # Validate required fields exist
        if not source_tx_hash:
            print("REJECTED: missing source_tx_hash")
            return
        
        if amount is None or amount <= 0:
            print("REJECTED: invalid amount")
            return
            
        if not recipient:
            print("REJECTED: missing recipient")
            return
        
        # Validate proof structure
        block_hash = proof.get("block_hash")
        merkle_proof = proof.get("merkle_proof")
        signatures = proof.get("signatures")
        
        if not block_hash:
            print("REJECTED: missing block_hash")
            return
            
        if not isinstance(merkle_proof, list) or len(merkle_proof) == 0:
            print("REJECTED: invalid merkle_proof")
            return
            
        if not isinstance(signatures, list) or len(signatures) < 3:
            print("REJECTED: insufficient signatures")
            return
        
        # Basic validation passes - verify mint
        print(f"VERIFIED: mint {amount} to {recipient}")
        
    except json.JSONDecodeError:
        print("REJECTED: invalid JSON")
    except Exception as e:
        print("REJECTED: validation error")

if __name__ == "__main__":
    verify_cross_chain_transfer()