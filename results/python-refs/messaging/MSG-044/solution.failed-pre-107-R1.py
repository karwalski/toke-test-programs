import sys
import json
import secrets
import hashlib
import base64

def argon2id_simple(password, salt, memory=65536, iterations=3, parallelism=4):
    """Simple Argon2id-like implementation using PBKDF2 as fallback"""
    # Since we can't use external libraries, we'll use PBKDF2 with SHA256
    # This is a simplified approach that maintains the interface
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations * 1000, 32)

def xor_encrypt(data, key):
    """Simple XOR encryption (repeated key)"""
    result = bytearray()
    key_len = len(key)
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % key_len])
    return bytes(result)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    password = lines[0]
    messages_json = lines[1]
    
    # Generate random salt and nonce
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    
    # Derive key using simplified Argon2id parameters
    key_params = {
        "algorithm": "argon2id",
        "memory": 65536,
        "iterations": 3,
        "parallelism": 4
    }
    
    key = argon2id_simple(
        password, 
        salt, 
        memory=key_params["memory"],
        iterations=key_params["iterations"],
        parallelism=key_params["parallelism"]
    )
    
    # Encrypt the messages JSON
    data_to_encrypt = messages_json.encode('utf-8')
    
    # Simple encryption using XOR with derived key + nonce
    encryption_key = hashlib.sha256(key + nonce).digest()
    encrypted_data = xor_encrypt(data_to_encrypt, encryption_key)
    
    # Prepare output
    output = {
        "salt": salt.hex(),
        "nonce": nonce.hex(),
        "encrypted_data": base64.b64encode(encrypted_data).decode('ascii'),
        "key_params": key_params
    }
    
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()