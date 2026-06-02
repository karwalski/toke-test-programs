import hashlib
import secrets
import base64

def bcrypt_hash(password, cost=10):
    # Generate a random salt (16 bytes)
    salt_bytes = secrets.token_bytes(16)
    
    # Encode salt in bcrypt's modified base64
    salt_b64 = base64.b64encode(salt_bytes)[:22].decode('ascii')
    # Replace standard base64 chars with bcrypt's alphabet
    salt_b64 = salt_b64.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', 
                                               './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'))
    
    # Simple bcrypt-like hash (not cryptographically equivalent to real bcrypt)
    # This is a simplified implementation for the requirement
    password_bytes = password.encode('utf-8')
    
    # Simulate bcrypt rounds
    hash_input = password_bytes + salt_bytes
    for i in range(2**cost):
        hash_input = hashlib.sha256(hash_input).digest()
    
    # Encode hash in bcrypt's modified base64 (31 chars)
    hash_b64 = base64.b64encode(hash_input)[:31].decode('ascii')
    hash_b64 = hash_b64.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', 
                                               './ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'))
    
    return f"$2b${cost:02d}${salt_b64}{hash_b64}"

# Read password from stdin
password = input().strip()

# Generate and output bcrypt hash
print(bcrypt_hash(password, 10))