import sys

# secp256k1 curve parameters
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0
B = 7
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def mod_inverse(a, m):
    """Compute modular inverse using extended Euclidean algorithm"""
    if a < 0:
        a = (a % m + m) % m
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def point_add(p1, p2):
    """Add two points on the elliptic curve"""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2:
        if y1 == y2:
            # Point doubling
            s = (3 * x1 * x1 + A) * mod_inverse(2 * y1, P) % P
        else:
            return None  # Point at infinity
    else:
        # Point addition
        s = (y2 - y1) * mod_inverse(x2 - x1, P) % P
    
    x3 = (s * s - x1 - x2) % P
    y3 = (s * (x1 - x3) - y1) % P
    
    return (x3, y3)

def point_multiply(k, point):
    """Multiply point by scalar k using double-and-add"""
    if k == 0:
        return None
    if k == 1:
        return point
    
    result = None
    addend = point
    
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    
    return result

def main():
    # Read input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    private_key_a = int(lines[0], 16)
    private_key_b = int(lines[1], 16)
    
    # Generator point
    G = (GX, GY)
    
    # Compute public keys
    pub_a = point_multiply(private_key_a, G)
    pub_b = point_multiply(private_key_b, G)
    
    # Compute shared secrets (should be the same)
    shared_point_a = point_multiply(private_key_a, pub_b)
    
    # Output the x-coordinate of the shared secret
    shared_secret_x = shared_point_a[0]
    print(f"{shared_secret_x:064x}")

if __name__ == "__main__":
    main()