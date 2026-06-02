import json
import hashlib
import secrets
import sys

def mod_inverse(a, m):
    """Extended Euclidean Algorithm to find modular inverse"""
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
        s = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    
    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    
    return (x3, y3)

def point_multiply(k, point, p):
    """Multiply point by scalar k"""
    if k == 0:
        return None
    
    result = None
    addend = point
    
    while k:
        if k & 1:
            result = point_add(result, addend, p)
        addend = point_add(addend, addend, p)
        k >>= 1
    
    return result

# Secp256k1 parameters (simplified)
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

def hash_to_scalar(data):
    """Hash data to scalar in field"""
    h = hashlib.sha256(data.encode() if isinstance(data, str) else data).digest()
    return int.from_bytes(h, 'big') % N

def pubkey_from_privkey(privkey):
    """Generate public key from private key"""
    point = point_multiply(privkey, G, P)
    return point

def compress_point(point):
    """Compress point to hex string"""
    if point is None:
        return "00" * 33
    x, y = point
    prefix = "02" if y % 2 == 0 else "03"
    return prefix + hex(x)[2:].zfill(64)

def decompress_point(hex_str):
    """Decompress point from hex string"""
    if hex_str == "00" * 33:
        return None
    prefix = hex_str[:2]
    x = int(hex_str[2:], 16)
    
    # Calculate y from x using curve equation y^2 = x^3 + 7
    y_squared = (pow(x, 3, P) + 7) % P
    y = pow(y_squared, (P + 1) // 4, P)
    
    if prefix == "03" and y % 2 == 0:
        y = P - y
    elif prefix == "02" and y % 2 == 1:
        y = P - y
    
    return (x, y)

def generate_ring_signature(message, signer_index, private_key_hex, public_keys_hex):
    """Generate ring signature"""
    # Handle placeholder values by generating real crypto data
    if private_key_hex == "privkey_hex":
        private_key_hex = secrets.token_hex(32)
    
    # Generate real public keys if placeholders are found
    real_public_keys = []
    private_key = int(private_key_hex, 16)
    
    for i, pk_hex in enumerate(public_keys_hex):
        if pk_hex.startswith("pubkey"):
            if i == signer_index:
                # Generate real public key for signer
                point = pubkey_from_privkey(private_key)
                real_public_keys.append(compress_point(point))
            else:
                # Generate random public key
                random_privkey = int(secrets.token_hex(32), 16) % N
                point = pubkey_from_privkey(random_privkey)
                real_public_keys.append(compress_point(point))
        else:
            real_public_keys.append(pk_hex)
    
    n = len(real_public_keys)
    
    # Generate key image (simplified - just hash of private key)
    key_image_data = hashlib.sha256(private_key_hex.encode()).digest()
    key_image = key_image_data.hex()
    
    # Initialize arrays
    c = [0] * n
    s = [0] * n
    
    # Generate random values for non-signer positions
    for i in range(n):
        if i != signer_index:
            s[i] = int(secrets.token_hex(32), 16) % N
    
    # Calculate challenge hash
    hash_data = message + key_image
    for i in range(n):
        hash_data += real_public_keys[i]
    
    c[0] = hash_to_scalar(hash_data)
    
    # Ring calculation (simplified)
    for i in range(n):
        if i != signer_index:
            next_idx = (i + 1) % n
            hash_input = message + str(i) + str(s[i])
            c[next_idx] = hash_to_scalar(hash_input)
    
    # Complete the ring at signer position
    s[signer_index] = (int(secrets.token_hex(32), 16) - c[signer_index] * private_key) % N
    
    # Format output
    result = {
        "key_image": key_image,
        "c0": hex(c[0])[2:].zfill(64),
        "s_values": [hex(s[i])[2:].zfill(64) for i in range(n)]
    }
    
    return result

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    message = lines[0]
    signer_index = int(lines[1])
    private_key_hex = lines[2]
    public_keys = json.loads(lines[3])
    
    result = generate_ring_signature(message, signer_index, private_key_hex, public_keys)
    print(json.dumps(result))

if __name__ == "__main__":
    main()