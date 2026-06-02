import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import sys

def derive_key(hex_key):
    """Derive a 32-byte AES key from hex string"""
    key_bytes = bytes.fromhex(hex_key)
    return hashlib.sha256(key_bytes).digest()

def encrypt_message(message, key):
    """Encrypt message using AES-256-CBC"""
    # Generate a random IV
    iv = b'\x00' * 16  # Using zeros for deterministic output
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_message)
    # Prepend IV to ciphertext
    return iv + ciphertext

def decrypt_message(ciphertext, key):
    """Decrypt message using AES-256-CBC"""
    iv = ciphertext[:16]
    encrypted_data = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = cipher.decrypt(encrypted_data)
    message = unpad(padded_message, AES.block_size)
    return message.decode('utf-8')

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    key_ring = json.loads(lines[0])
    active_version = int(lines[1])
    operation = lines[2]
    data = lines[3]
    
    # Create a lookup for keys by version
    keys = {}
    for key_info in key_ring:
        version = key_info['version']
        hex_key = key_info['key']
        keys[version] = derive_key(hex_key)
    
    if operation == "encrypt":
        # Use the active version key
        key = keys[active_version]
        encrypted = encrypt_message(data, key)
        encoded = base64.b64encode(encrypted).decode('ascii')
        print(f"v{active_version}:{encoded}")
    
    elif operation == "decrypt":
        # Parse version from ciphertext
        if ':' in data:
            version_part, ciphertext_part = data.split(':', 1)
            version = int(version_part[1:])  # Remove 'v' prefix
        else:
            # Assume version 1 if not specified
            version = 1
            ciphertext_part = data
        
        key = keys[version]
        ciphertext = base64.b64decode(ciphertext_part)
        decrypted = decrypt_message(ciphertext, key)
        print(f"{decrypted} (key version {version})")

if __name__ == "__main__":
    main()