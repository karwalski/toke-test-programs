import hashlib

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
        return None
    return (x % m + m) % m

def point_add(p1, p2, p):
    """Add two points on elliptic curve y^2 = x^3 + 7 (mod p)"""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2:
        if y1 == y2:
            # Point doubling
            s = (3 * x1 * x1 * mod_inverse(2 * y1, p)) % p
        else:
            return None  # Point at infinity
    else:
        # Point addition
        s = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    
    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    
    return (x3, y3)

def point_multiply(k, point, p):
    """Multiply point by scalar k using double-and-add"""
    if k == 0:
        return None
    if k == 1:
        return point
    
    result = None
    addend = point
    
    while k:
        if k & 1:
            result = point_add(result, addend, p)
        addend = point_add(addend, addend, p)
        k >>= 1
    
    return result

def decompress_pubkey(pubkey_hex):
    """Decompress compressed public key or parse uncompressed"""
    pubkey_bytes = bytes.fromhex(pubkey_hex)
    
    # secp256k1 parameters
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    
    if len(pubkey_bytes) == 33:  # Compressed
        prefix = pubkey_bytes[0]
        x = int.from_bytes(pubkey_bytes[1:], 'big')
        
        # Calculate y^2 = x^3 + 7 (mod p)
        y_squared = (pow(x, 3, p) + 7) % p
        
        # Calculate square root using Tonelli-Shanks or direct method
        # For secp256k1, p ≡ 3 (mod 4), so we can use y = ±y_squared^((p+1)/4)
        y = pow(y_squared, (p + 1) // 4, p)
        
        # Choose correct y based on prefix
        if (y % 2) != (prefix - 2):
            y = p - y
        
        return (x, y)
    
    elif len(pubkey_bytes) == 65:  # Uncompressed
        x = int.from_bytes(pubkey_bytes[1:33], 'big')
        y = int.from_bytes(pubkey_bytes[33:], 'big')
        return (x, y)
    
    else:
        raise ValueError("Invalid public key format")

def verify_signature(pubkey_hex, message, r_hex, s_hex):
    """Verify ECDSA signature"""
    try:
        # secp256k1 parameters
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
             0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
        
        # Parse inputs
        pubkey_point = decompress_pubkey(pubkey_hex)
        r = int(r_hex, 16)
        s = int(s_hex, 16)
        
        # Check r and s are in valid range
        if r <= 0 or r >= n or s <= 0 or s >= n:
            return False
        
        # Calculate message hash
        message_hash = hashlib.sha256(message.encode()).digest()
        z = int.from_bytes(message_hash, 'big')
        
        # Calculate signature verification
        w = mod_inverse(s, n)
        if w is None:
            return False
        
        u1 = (z * w) % n
        u2 = (r * w) % n
        
        # Calculate point u1*G + u2*pubkey
        point1 = point_multiply(u1, G, p)
        point2 = point_multiply(u2, pubkey_point, p)
        result_point = point_add(point1, point2, p)
        
        if result_point is None:
            return False
        
        # Check if x coordinate matches r
        return result_point[0] % n == r
        
    except Exception:
        return False

# Read input
pubkey_hex = input().strip()
message = input().strip()
r_hex = input().strip()
s_hex = input().strip()

# Verify signature
if verify_signature(pubkey_hex, message, r_hex, s_hex):
    print("VALID")
else:
    print("INVALID")