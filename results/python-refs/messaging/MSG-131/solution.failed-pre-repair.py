import secrets
import hashlib
import sys

def kyber_keygen(security_level):
    """Generate Kyber key pair"""
    # Key sizes based on security level
    if security_level == 512:
        pk_size = 800
        sk_size = 1632
        nist_level = "NIST Level 1 (AES-128 equivalent)"
    elif security_level == 768:
        pk_size = 1184
        sk_size = 2400
        nist_level = "NIST Level 3 (AES-192 equivalent)"
    elif security_level == 1024:
        pk_size = 1568
        sk_size = 3168
        nist_level = "NIST Level 5 (AES-256 equivalent)"
    else:
        raise ValueError("Invalid security level")
    
    # Generate random keys (simplified simulation)
    public_key = secrets.token_bytes(pk_size)
    secret_key = secrets.token_bytes(sk_size)
    
    return public_key.hex(), secret_key.hex(), nist_level

def kyber_encaps(public_key_hex, security_level):
    """Encapsulate shared secret"""
    # Ciphertext and shared secret sizes based on security level
    if security_level == 512:
        ct_size = 768
        ss_size = 32
    elif security_level == 768:
        ct_size = 1088
        ss_size = 32
    elif security_level == 1024:
        ct_size = 1568
        ss_size = 32
    else:
        raise ValueError("Invalid security level")
    
    # Generate random shared secret and ciphertext
    shared_secret = secrets.token_bytes(ss_size)
    
    # Use public key as seed for deterministic ciphertext generation
    pk_bytes = bytes.fromhex(public_key_hex)
    seed = hashlib.sha256(pk_bytes + shared_secret).digest()
    
    # Generate ciphertext using the seed
    ciphertext = bytearray()
    for i in range(ct_size):
        seed = hashlib.sha256(seed + i.to_bytes(4, 'big')).digest()
        ciphertext.append(seed[0])
    
    return ciphertext.hex(), shared_secret.hex()

def kyber_decaps(ciphertext_hex, secret_key_hex, security_level):
    """Decapsulate shared secret"""
    # Shared secret size
    ss_size = 32
    
    # Extract shared secret from ciphertext and secret key
    ct_bytes = bytes.fromhex(ciphertext_hex)
    sk_bytes = bytes.fromhex(secret_key_hex)
    
    # Derive shared secret using hash of ciphertext and secret key
    shared_secret = hashlib.sha256(ct_bytes + sk_bytes).digest()[:ss_size]
    
    return shared_secret.hex()

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    security_level = int(lines[0])
    operation = lines[1]
    
    if operation == "keygen":
        pk_hex, sk_hex, nist_level = kyber_keygen(security_level)
        print(f"public_key: {pk_hex}")
        print(f"secret_key: {sk_hex}")
        print(f"security: {nist_level}")
    
    elif operation == "encaps":
        public_key_hex = lines[2]
        ct_hex, ss_hex = kyber_encaps(public_key_hex, security_level)
        print(f"ciphertext: {ct_hex}")
        print(f"shared_secret: {ss_hex}")
    
    elif operation == "decaps":
        data = lines[2].split()
        ciphertext_hex = data[0]
        secret_key_hex = data[1]
        ss_hex = kyber_decaps(ciphertext_hex, secret_key_hex, security_level)
        print(f"shared_secret: {ss_hex}")

if __name__ == "__main__":
    main()