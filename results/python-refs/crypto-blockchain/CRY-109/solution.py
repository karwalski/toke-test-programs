import hashlib
import hmac
import base64

def base58_decode(s):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    decoded = 0
    multi = 1
    for char in reversed(s):
        decoded += multi * alphabet.index(char)
        multi *= 58
    
    h = hex(decoded)[2:]
    if len(h) % 2:
        h = '0' + h
    res = bytes.fromhex(h)
    
    # Handle leading zeros
    pad = 0
    for c in s:
        if c == alphabet[0]:
            pad += 1
        else:
            break
    return b'\x00' * pad + res

def wif_to_private_key(wif):
    decoded = base58_decode(wif)
    # Remove version byte (0x80) and checksum (last 4 bytes)
    private_key = decoded[1:-4]
    if len(private_key) == 33 and private_key[-1] == 0x01:
        private_key = private_key[:-1]  # Remove compression flag
    return private_key

def sha256(data):
    return hashlib.sha256(data).digest()

def double_sha256(data):
    return sha256(sha256(data))

def mod_inverse(a, m):
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

def point_add(p1, p2, p):
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
        s = ((y2 - y1) * mod_inverse((x2 - x1) % p, p)) % p
    
    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    
    return (x3, y3)

def point_multiply(k, point, p):
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

def sign_message(private_key, message):
    # Bitcoin message signing
    message_prefix = b"\x18Bitcoin Signed Message:\n"
    message_bytes = message.encode('utf-8')
    message_length = len(message_bytes)
    
    if message_length < 253:
        length_bytes = bytes([message_length])
    elif message_length < 0x10000:
        length_bytes = b'\xfd' + message_length.to_bytes(2, 'little')
    else:
        length_bytes = b'\xfe' + message_length.to_bytes(4, 'little')
    
    full_message = message_prefix + length_bytes + message_bytes
    message_hash = double_sha256(full_message)
    
    # Secp256k1 parameters
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    g = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
         0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    
    private_key_int = int.from_bytes(private_key, 'big')
    message_hash_int = int.from_bytes(message_hash, 'big')
    
    # Generate public key
    public_key_point = point_multiply(private_key_int, g, p)
    
    # Sign with ECDSA
    for recovery_id in range(4):
        k = 1  # Deterministic k for reproducible results
        k_point = point_multiply(k, g, p)
        r = k_point[0] % n
        
        if r == 0:
            continue
            
        k_inv = mod_inverse(k, n)
        s = (k_inv * (message_hash_int + r * private_key_int)) % n
        
        if s == 0:
            continue
        
        # Ensure low s value
        if s > n // 2:
            s = n - s
            recovery_id ^= 1
        
        # Check recovery
        recovered_point = recover_public_key(message_hash, r, s, recovery_id, g, n, p)
        if recovered_point == public_key_point:
            # Format signature
            signature = bytes([27 + recovery_id]) + r.to_bytes(32, 'big') + s.to_bytes(32, 'big')
            return base64.b64encode(signature).decode('ascii')
    
    raise Exception("Could not create recoverable signature")

def recover_public_key(message_hash, r, s, recovery_id, g, n, p):
    x = r + (recovery_id // 2) * n
    
    # Calculate y
    y_squared = (pow(x, 3, p) + 7) % p
    y = pow(y_squared, (p + 1) // 4, p)
    
    if y % 2 != recovery_id % 2:
        y = p - y
    
    R = (x, y)
    
    message_hash_int = int.from_bytes(message_hash, 'big')
    r_inv = mod_inverse(r, n)
    
    # Calculate point
    point1 = point_multiply((message_hash_int * r_inv) % n, g, p)
    point2 = point_multiply((s * r_inv) % n, R, p)
    
    if point1:
        point1 = (point1[0], (-point1[1]) % p)
    
    return point_add(point1, point2, p)

# Read input
wif = input().strip()
message = input().strip()

# Convert WIF to private key
private_key = wif_to_private_key(wif)

# Sign message
signature = sign_message(private_key, message)

print(signature)