import json
import sys
import hashlib

def main():
    # Read input
    validators_json = input().strip()
    seed_hex = input().strip()
    
    # Parse validators
    validators = json.loads(validators_json)
    
    # Calculate total stake
    total_stake = sum(v["stake"] for v in validators)
    
    # Convert seed to bytes and hash it to get a deterministic random number
    seed_bytes = bytes.fromhex(seed_hex)
    hash_obj = hashlib.sha256(seed_bytes)
    hash_bytes = hash_obj.digest()
    
    # Convert first 8 bytes of hash to integer
    random_int = int.from_bytes(hash_bytes[:8], byteorder='big')
    
    # Get a value between 0 and total_stake-1
    random_stake = random_int % total_stake
    
    # Select validator based on weighted stake
    current_stake = 0
    for validator in validators:
        current_stake += validator["stake"]
        if random_stake < current_stake:
            print(validator["validator"])
            return

if __name__ == "__main__":
    main()