import hashlib
import sys

def sha512(data):
    return hashlib.sha512(data).digest()

def mod_inverse(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    return (x % m + m) % m

def point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    
    x1, y1 = p1
    x2, y2 = p2
    
    # Ed25519 curve parameters
    p = 2**255 - 19
    d = 37095705934669439343138083508754565189542113879843219016388785533085940283555
    
    x1x2 = (x1 * x2) % p
    y1y2 = (y1 * y2) % p
    dx1x2y1y2 = (d * x1x2 * y1y2) % p
    
    x3 = ((x1 * y2 + y1 * x2) * mod_inverse(1 + dx1x2y1y2, p)) % p
    y3 = ((y1y2 - x1x2) * mod_inverse(1 - dx1x2y1y2, p)) % p
    
    return (x3, y3)

def scalar_mult(k, point):
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

def bytes_to_int(b):
    return int.from_bytes(b, 'little')

def int_to_bytes(n, length):
    return n.to_bytes(length, 'little')

def point_encode(point):
    if point is None:
        return b'\x00' * 32
    
    x, y = point
    p = 2**255 - 19
    
    y_bytes = int_to_bytes(y % p, 32)
    if x % 2:
        y_bytes = bytes([y_bytes[31] | 0x80]) + y_bytes[:31]
    
    return y_bytes

def ed25519_sign(private_seed, message):
    # Hash the private seed
    h = sha512(private_seed)
    
    # Extract scalar and prefix
    a = bytes_to_int(h[:32])
    a &= (1 << 254) - 8
    a |= (1 << 254)
    
    prefix = h[32:64]
    
    # Ed25519 base point
    Bx = 15112221349535400772501151409588531511454012693041857206046113283949847762202
    By = 46316835694926478169428394003475163141307993866256225615783033603165251855960
    B = (Bx, By)
    
    # Compute public key A = [a]B
    A = scalar_mult(a, B)
    
    # Compute r
    r_hash = sha512(prefix + message)
    r = bytes_to_int(r_hash) % (2**252 + 27742317777372353535851937790883648493)
    
    # Compute R = [r]B
    R = scalar_mult(r, B)
    
    # Encode points
    R_encoded = point_encode(R)
    A_encoded = point_encode(A)
    
    # Compute S
    k_hash = sha512(R_encoded + A_encoded + message)
    k = bytes_to_int(k_hash) % (2**252 + 27742317777372353535851937790883648493)
    
    S = (r + k * a) % (2**252 + 27742317777372353535851937790883648493)
    S_encoded = int_to_bytes(S, 32)
    
    # Return signature
    return R_encoded + S_encoded

# Read input
seed_hex = input().strip()
message = input().encode('utf-8')

# Convert seed to bytes
private_seed = bytes.fromhex(seed_hex)

# Generate signature
signature = ed25519_sign(private_seed, message)

# Output as hex
print(signature.hex())