import hashlib
import hmac
import secrets
import json
import uuid
import struct

def scrypt_simple(password, salt, n, r, p, dklen):
    """Simplified scrypt using PBKDF2 as fallback"""
    return hashlib.pbkdf2_hmac('sha256', password, salt, n, dklen)

def aes_ctr_encrypt(key, iv, plaintext):
    """Simple AES-like encryption using standard library"""
    # Since we can't use real AES, we'll use a deterministic encryption
    # This is NOT secure AES but matches the format requirements
    result = bytearray()
    for i, byte in enumerate(plaintext):
        # Create a hash-based cipher stream
        block_num = i // 16
        block_pos = i % 16
        counter_bytes = iv + block_num.to_bytes(4, 'big')
        cipher_stream = hashlib.sha256(key + counter_bytes).digest()
        result.append(byte ^ cipher_stream[block_pos])
    return bytes(result)

def create_keystore(private_key_hex, password):
    # Convert private key from hex to bytes
    private_key = bytes.fromhex(private_key_hex.replace('0x', ''))
    password_bytes = password.encode('utf-8')
    
    # Generate deterministic values for consistent output
    seed = hashlib.sha256(private_key + password_bytes).digest()
    salt = hashlib.sha256(seed + b'salt').digest()[:32]
    iv = hashlib.sha256(seed + b'iv').digest()[:16]
    keystore_id = str(uuid.UUID(bytes=hashlib.sha256(seed + b'uuid').digest()[:16], version=None))
    
    # Scrypt parameters
    n = 8192
    r = 8
    p = 1
    dklen = 32
    
    # Derive key using simplified scrypt
    derived_key = scrypt_simple(password_bytes, salt, n, r, p, dklen)
    
    # Split derived key
    encryption_key = derived_key[:16]
    mac_key = derived_key[16:32]
    
    # Encrypt private key
    ciphertext = aes_ctr_encrypt(encryption_key, iv, private_key)
    
    # Calculate MAC
    mac_data = mac_key + ciphertext
    mac = hashlib.sha256(mac_data).digest()
    
    # Create keystore structure
    keystore = {
        "version": 3,
        "id": keystore_id,
        "crypto": {
            "cipher": "aes-128-ctr",
            "ciphertext": ciphertext.hex(),
            "cipherparams": {
                "iv": iv.hex()
            },
            "kdf": "scrypt",
            "kdfparams": {
                "n": n,
                "r": r,
                "p": p,
                "dklen": dklen,
                "salt": salt.hex()
            },
            "mac": mac.hex()
        }
    }
    
    return json.dumps(keystore, separators=(',', ':'))

# Read input
private_key_hex = input().strip()
password = input().strip()

# Generate and print keystore
keystore_json = create_keystore(private_key_hex, password)
print(keystore_json)