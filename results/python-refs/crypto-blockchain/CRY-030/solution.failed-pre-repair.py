import hashlib
import hmac
import secrets

def mod_inverse(a, m):
    """Calculate modular inverse using extended Euclidean algorithm"""
    if a < 0:
        a = (a % m + m) % m
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m

def point_multiply(k, x, y, p, a):
    """Multiply point (x, y) by scalar k on elliptic curve"""
    if k == 0:
        return None, None
    
    if k == 1:
        return x, y
    
    # Double-and-add algorithm
    result_x, result_y = None, None
    addend_x, addend_y = x, y
    
    while k:
        if k & 1:
            if result_x is None:
                result_x, result_y = addend_x, addend_y
            else:
                result_x, result_y = point_add(result_x, result_y, addend_x, addend_y, p, a)
        
        addend_x, addend_y = point_double(addend_x, addend_y, p, a)
        k >>= 1
    
    return result_x, result_y

def point_add(x1, y1, x2, y2, p, a):
    """Add two points on elliptic curve"""
    if x1 == x2:
        if y1 == y2:
            return point_double(x1, y1, p, a)
        else:
            return None, None  # Point at infinity
    
    s = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    
    return x3, y3

def point_double(x, y, p, a):
    """Double a point on elliptic curve"""
    s = ((3 * x * x + a) * mod_inverse(2 * y, p)) % p
    x3 = (s * s - 2 * x) % p
    y3 = (s * (x - x3) - y) % p
    
    return x3, y3

def ecdsa_sign(private_key, message_hash, p, n, gx, gy, a):
    """Sign message hash with ECDSA"""
    # Use deterministic k based on RFC 6979 (simplified)
    # For test purposes, use a simple deterministic approach
    k_bytes = hmac.new(private_key.to_bytes(32, 'big'), message_hash, hashlib.sha256).digest()
    k = int.from_bytes(k_bytes, 'big') % n
    if k == 0:
        k = 1
    
    # Calculate r = (k * G).x mod n
    rx, ry = point_multiply(k, gx, gy, p, a)
    r = rx % n
    
    if r == 0:
        # In practice, we'd try again with different k
        r = 1
    
    # Calculate s = k^-1 * (hash + r * private_key) mod n
    z = int.from_bytes(message_hash, 'big')
    s = (mod_inverse(k, n) * (z + r * private_key)) % n
    
    if s == 0:
        s = 1
    
    return r, s

# secp256k1 parameters
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
a = 0

# Read input
private_key_hex = input().strip()
message = input().strip()

# Convert private key from hex
private_key = int(private_key_hex, 16)

# Hash the message
message_hash = hashlib.sha256(message.encode()).digest()

# Sign the message
r, s = ecdsa_sign(private_key, message_hash, p, n, gx, gy, a)

# Output the signature
print(f"r={r:064x}")
print(f"s={s:064x}")