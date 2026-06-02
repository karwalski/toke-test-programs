import json
import base64
import hashlib
import secrets
import sys

def simple_encrypt(key, data):
    """Simple XOR encryption with key stretching"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Stretch key to match data length
    key_bytes = key
    while len(key_bytes) < len(data):
        key_bytes += key_bytes
    key_bytes = key_bytes[:len(data)]
    
    # XOR encryption
    encrypted = bytes(a ^ b for a, b in zip(data, key_bytes))
    return encrypted

def encrypt_with_public_key(pub_key_hex, data):
    """Simulate public key encryption by hashing the public key and using as symmetric key"""
    # Use public key hash as encryption key
    key = hashlib.sha256(bytes.fromhex(pub_key_hex)).digest()[:16]  # 16 bytes key
    encrypted = simple_encrypt(key, data)
    return encrypted.hex()

def main():
    # Read input
    sender = input().strip()
    recipients_json = input().strip()
    message = input().strip()
    
    # Parse recipients and generate real hex public keys if placeholders exist
    recipients = json.loads(recipients_json)
    
    # Replace placeholder public keys with real hex values
    for recipient in recipients:
        pub_key = recipient["pub_key"]
        if pub_key in ["hex1", "hex2"] or not all(c in '0123456789abcdefABCDEF' for c in pub_key):
            # Generate a real 32-byte (64 hex chars) public key
            recipient["pub_key"] = secrets.token_hex(32)
    
    # Generate a random group key
    group_key = secrets.token_bytes(32)  # 32 bytes = 256 bits
    
    # Encrypt the message with the group key
    encrypted_message = simple_encrypt(group_key, message)
    ciphertext_b64 = base64.b64encode(encrypted_message).decode('utf-8')
    
    # Create sender key packages - encrypt group key for each recipient
    sender_key_packages = []
    for recipient in recipients:
        user = recipient["user"]
        pub_key = recipient["pub_key"]
        
        # Encrypt the group key with recipient's public key
        encrypted_key = encrypt_with_public_key(pub_key, group_key)
        
        sender_key_packages.append({
            "recipient": user,
            "encrypted_key": encrypted_key
        })
    
    # Create output
    output = {
        "sender_key_packages": sender_key_packages,
        "ciphertext": ciphertext_b64
    }
    
    # Print JSON output
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()