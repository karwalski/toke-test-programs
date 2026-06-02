import hashlib
import hmac
import sys

def hmac_sha512(key, data):
    return hmac.new(key, data, hashlib.sha512).digest()

def derive_master_key(seed_hex):
    seed = bytes.fromhex(seed_hex)
    master = hmac_sha512(b"ed25519 seed", seed)
    master_private_key = master[:32]
    master_chain_code = master[32:]
    return master_private_key, master_chain_code

def derive_child_key(parent_private_key, parent_chain_code, index):
    if index >= 2**31:  # hardened derivation
        data = b'\x00' + parent_private_key + index.to_bytes(4, 'big')
    else:  # non-hardened derivation
        # For simplicity, we'll treat all as hardened since we only have private key
        data = b'\x00' + parent_private_key + index.to_bytes(4, 'big')
    
    child = hmac_sha512(parent_chain_code, data)
    child_private_key = child[:32]
    child_chain_code = child[32:]
    return child_private_key, child_chain_code

def parse_path(path):
    if not path.startswith('m/'):
        raise ValueError("Invalid derivation path")
    
    if path == 'm':
        return []
    
    parts = path[2:].split('/')
    indices = []
    
    for part in parts:
        if part.endswith("'"):
            index = int(part[:-1]) + 2**31  # hardened
        else:
            index = int(part)
        indices.append(index)
    
    return indices

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    seed_hex = lines[0]
    derivation_path = lines[1]
    
    # Derive master key
    private_key, chain_code = derive_master_key(seed_hex)
    
    # Parse and apply derivation path
    indices = parse_path(derivation_path)
    
    for index in indices:
        private_key, chain_code = derive_child_key(private_key, chain_code, index)
    
    # Output results
    print(private_key.hex())
    print(chain_code.hex())

if __name__ == "__main__":
    main()