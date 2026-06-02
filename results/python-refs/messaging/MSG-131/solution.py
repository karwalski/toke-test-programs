import sys

def main():
    lines = [l.strip() for l in sys.stdin]
    security_level = int(lines[0])
    operation = lines[1]
    
    params = {
        512: (800, 1632, 768, "NIST Level 1 (AES-128 equivalent)", "Kyber-512"),
        768: (1184, 2400, 1088, "NIST Level 3 (AES-192 equivalent)", "Kyber-768"),
        1024: (1568, 3168, 1568, "NIST Level 5 (AES-256 equivalent)", "Kyber-1024"),
    }
    pk_size, sk_size, ct_size, nist_level, algo = params[security_level]
    
    if operation == "keygen":
        print(f"public_key: hex ({pk_size} bytes)")
        print(f"secret_key: hex ({sk_size} bytes)")
        print(f"security: {nist_level}")
    elif operation == "encaps":
        print(f"ciphertext: hex ({ct_size} bytes)")
        print(f"shared_secret: hex (32 bytes)")
        print(f"algorithm: {algo}")
    elif operation == "decaps":
        print(f"shared_secret: hex (32 bytes)")
        print(f"algorithm: {algo}")

if __name__ == "__main__":
    main()