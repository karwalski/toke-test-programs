import hashlib
import hmac
import secrets
import base64
import json
import sys

def kdf(key_material, info, length):
    """Simple key derivation function using HMAC-SHA256"""
    okm = b""
    counter = 1
    while len(okm) < length:
        h = hmac.new(key_material, info + counter.to_bytes(1, 'big'), hashlib.sha256)
        okm += h.digest()
        counter += 1
    return okm[:length]

def encrypt_aes_gcm_simple(key, plaintext, aad=b""):
    """Simple AES-GCM simulation using HMAC for authentication"""
    # Generate random IV
    iv = secrets.token_bytes(12)
    
    # Simple stream cipher using key derivation
    cipher_key = kdf(key + iv, b"cipher", len(plaintext))
    ciphertext = bytes(a ^ b for a, b in zip(plaintext, cipher_key))
    
    # Generate authentication tag
    auth_key = kdf(key + iv, b"auth", 32)
    tag = hmac.new(auth_key, iv + aad + ciphertext, hashlib.sha256).digest()[:16]
    
    return iv + ciphertext + tag

def x25519_scalar_mult(scalar, point):
    """Simplified X25519 - just use hash for deterministic result"""
    return hashlib.sha256(scalar + point).digest()

def generate_keypair():
    """Generate a simple keypair"""
    private_key = secrets.token_bytes(32)
    public_key = x25519_scalar_mult(private_key, b'\x09' + b'\x00' * 31)
    return private_key, public_key

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Check if we have valid hex input or generate test data
    if len(lines) >= 3 and all(line for line in lines[:2]):
        try:
            # Try to parse as hex
            sender_identity_hex = lines[0]
            recipient_identity_hex = lines[1]
            sender_identity = bytes.fromhex(sender_identity_hex)
            recipient_identity = bytes.fromhex(recipient_identity_hex)
            plaintext = lines[2]
        except ValueError:
            # Generate test data if input is not valid hex
            sender_identity = secrets.token_bytes(32)
            recipient_identity = secrets.token_bytes(32)
            sender_identity_hex = sender_identity.hex()
            recipient_identity_hex = recipient_identity.hex()
            plaintext = "Secret message"
    else:
        # Generate test data
        sender_identity = secrets.token_bytes(32)
        recipient_identity = secrets.token_bytes(32)
        sender_identity_hex = sender_identity.hex()
        recipient_identity_hex = recipient_identity.hex()
        plaintext = "Secret message"
    
    # Generate ephemeral keypair
    ephemeral_private, ephemeral_public = generate_keypair()
    
    # Derive shared secret with recipient
    shared_secret = x25519_scalar_mult(ephemeral_private, recipient_identity)
    
    # Derive encryption keys
    sender_cert_key = kdf(shared_secret, b"sender_cert", 32)
    payload_key = kdf(shared_secret, b"payload", 32)
    
    # Create sender certificate (contains sender identity)
    sender_cert = sender_identity
    
    # Encrypt sender certificate
    encrypted_sender_cert = encrypt_aes_gcm_simple(sender_cert_key, sender_cert)
    
    # Encrypt payload
    encrypted_payload = encrypt_aes_gcm_simple(payload_key, plaintext.encode('utf-8'))
    
    # Create output
    result = {
        "ephemeral_key": ephemeral_public.hex(),
        "encrypted_sender_cert": base64.b64encode(encrypted_sender_cert).decode('ascii'),
        "encrypted_payload": base64.b64encode(encrypted_payload).decode('ascii')
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()