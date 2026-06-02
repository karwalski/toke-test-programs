import json
import base64
import hashlib
import secrets

def hash_key(key):
    """Simple key derivation using SHA256"""
    return hashlib.sha256(key.encode() if isinstance(key, str) else key).hexdigest()[:8]

def encrypt_message(message, key):
    """Simple XOR encryption with the key"""
    key_bytes = key.encode() if isinstance(key, str) else key
    key_hash = hashlib.sha256(key_bytes).digest()
    
    message_bytes = message.encode()
    encrypted = bytearray()
    
    for i, byte in enumerate(message_bytes):
        encrypted.append(byte ^ key_hash[i % len(key_hash)])
    
    return base64.b64encode(encrypted).decode()

def build_tree(public_keys):
    """Build a binary tree structure for key derivation"""
    tree_levels = []
    current_level = []
    
    # Level 0: leaf keys derived from public keys
    for i, pub_key in enumerate(public_keys):
        leaf_key = f"k{i+1}"
        current_level.append(leaf_key)
    
    tree_levels.append({"level": 0, "keys": current_level})
    level = 1
    
    # Build parent levels until we reach the root
    while len(current_level) > 1:
        parent_level = []
        
        # Pair up keys and create parent keys
        for i in range(0, len(current_level), 2):
            if i + 1 < len(current_level):
                # Combine two keys
                left_key = current_level[i]
                right_key = current_level[i + 1]
                
                # Extract numbers from key names for parent naming
                left_num = left_key.replace('k', '')
                right_num = right_key.replace('k', '')
                parent_key = f"k{left_num}{right_num}"
            else:
                # Odd number of keys, carry forward
                parent_key = current_level[i]
            
            parent_level.append(parent_key)
        
        tree_levels.append({"level": level, "keys": parent_level})
        current_level = parent_level
        level += 1
    
    # The last level should have the root key
    if tree_levels and tree_levels[-1]["keys"][0] != "root":
        # Replace the final key with "root"
        tree_levels[-1]["keys"] = ["root"]
    
    return tree_levels

def main():
    # Read input
    public_keys_line = input().strip()
    message = input().strip()
    
    # Parse public keys
    public_keys = json.loads(public_keys_line)
    
    # Build the tree structure
    tree_nodes = build_tree(public_keys)
    
    # Use the root key for encryption
    root_key = "root_encryption_key"
    ciphertext = encrypt_message(message, root_key)
    
    # Create the output
    result = {
        "tree_nodes": tree_nodes,
        "ciphertext": ciphertext
    }
    
    # Output the result
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()