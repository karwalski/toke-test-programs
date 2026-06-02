import sys
import hashlib
import secrets

def schnorr_prove(p, g, x):
    # Generate random k
    k = secrets.randbelow(p - 1) + 1
    
    # Compute commitment: r = g^k mod p
    r = pow(g, k, p)
    
    # Compute challenge: c = H(r) mod (p-1)
    hash_input = str(r).encode()
    hash_digest = hashlib.sha256(hash_input).digest()
    c = int.from_bytes(hash_digest, 'big') % (p - 1)
    
    # Compute response: s = k + c*x mod (p-1)
    s = (k + c * x) % (p - 1)
    
    return r, c, s

def schnorr_verify(p, g, y, r, c, s):
    # Verify: g^s = r * y^c mod p
    left = pow(g, s, p)
    right = (r * pow(y, c, p)) % p
    return left == right

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    p = int(lines[0])
    g = int(lines[1])
    x = int(lines[2])
    operation = lines[3]
    
    if operation == "PROVE":
        r, c, s = schnorr_prove(p, g, x)
        print(f"{r},{c},{s}")
    elif operation == "VERIFY":
        r = int(lines[4])
        c = int(lines[5])
        s = int(lines[6])
        y = int(lines[7])
        
        if schnorr_verify(p, g, y, r, c, s):
            print("VALID")
        else:
            print("INVALID")

if __name__ == "__main__":
    main()