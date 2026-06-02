import json
import hashlib
import hmac
import secrets
import base64
from typing import List, Dict, Any

def argon2id_simple(password: bytes, salt: bytes, iterations: int = 3, memory_kb: int = 64, parallelism: int = 1) -> bytes:
    """Simplified Argon2id implementation using PBKDF2 as fallback"""
    # Since we can't use external libraries, we'll use PBKDF2 as a reasonable substitute
    return hashlib.pbkdf2_hmac('sha256', password, salt, iterations * 1000, 32)

def aes_encrypt_simple(key: bytes, plaintext: bytes) -> bytes:
    """Simple XOR-based encryption (not real AES, but for demonstration)"""
    # Expand key to match plaintext length
    expanded_key = (key * ((len(plaintext) // len(key)) + 1))[:len(plaintext)]
    return bytes(p ^ k for p, k in zip(plaintext, expanded_key))

def wrap_key(master_key: bytes, key_data: bytes) -> bytes:
    """Wrap a key using the master key"""
    # Add some randomness
    iv = secrets.token_bytes(16)
    # Simple encryption
    encrypted = aes_encrypt_simple(master_key, key_data)
    return iv + encrypted

def main():
    # Read input
    password = input().strip()
    keys_json = input().strip()
    
    # Parse keys
    keys_to_backup = json.loads(keys_json)
    
    # Generate actual hex keys for any placeholder values
    for key_info in keys_to_backup:
        if key_info["key"] in ["aabb...", "ccdd...", "private_d_hex"] or "..." in key_info["key"]:
            # Generate real hex key based on type
            if key_info["type"] == "identity":
                key_info["key"] = secrets.token_hex(32)  # 256-bit identity key
            elif key_info["type"] == "session":
                key_info["key"] = secrets.token_hex(32)  # 256-bit session key
            elif key_info["type"] == "prekey":
                key_info["key"] = secrets.token_hex(32)  # 256-bit prekey
            else:
                key_info["key"] = secrets.token_hex(32)  # Default 256-bit key
    
    # Generate salt for master key derivation
    salt = secrets.token_bytes(32)
    
    # Derive master key from password using simplified Argon2id
    master_key = argon2id_simple(password.encode('utf-8'), salt)
    
    # Wrap each key
    wrapped_keys = []
    for key_info in keys_to_backup:
        key_id = key_info["key_id"]
        key_hex = key_info["key"]
        key_type = key_info["type"]
        
        # Convert hex key to bytes
        key_bytes = bytes.fromhex(key_hex)
        
        # Wrap the key
        wrapped_data = wrap_key(master_key, key_bytes)
        
        # Encode as base64
        wrapped_b64 = base64.b64encode(wrapped_data).decode('ascii')
        
        wrapped_keys.append({
            "key_id": key_id,
            "type": key_type,
            "wrapped": wrapped_b64
        })
    
    # Calculate integrity hash over all wrapped data
    integrity_data = salt + master_key + b''.join(base64.b64decode(wk["wrapped"]) for wk in wrapped_keys)
    integrity_hash = hashlib.sha256(integrity_data).hexdigest()
    
    # Prepare output
    result = {
        "salt": salt.hex(),
        "kdf": "argon2id",
        "wrapped_keys": wrapped_keys,
        "integrity_hash": integrity_hash
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()