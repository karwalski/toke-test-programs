import hashlib
import base64
import sys

def base58_decode(s):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    base_count = len(alphabet)
    decoded = 0
    multi = 1
    
    for char in reversed(s):
        if char not in alphabet:
            raise ValueError("Invalid character")
        decoded += multi * alphabet.index(char)
        multi *= base_count
    
    # Convert to bytes
    h = hex(decoded)[2:]
    if len(h) % 2:
        h = '0' + h
    
    # Count leading zeros
    leading_zeros = 0
    for c in s:
        if c == '1':
            leading_zeros += 1
        else:
            break
    
    return bytes([0] * leading_zeros) + bytes.fromhex(h)

def sha256(data):
    return hashlib.sha256(data).digest()

def hash160(data):
    return hashlib.new('ripemd160', sha256(data)).digest()

def point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2:
        if y1 == y2:
            # Point doubling
            s = (3 * x1 * x1 * pow(2 * y1, p - 2, p)) % p
        else:
            return None  # Point at infinity
    else:
        s = ((y2 - y1) * pow(x2 - x1, p - 2, p)) % p
    
    x3 = (s * s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    
    return (x3, y3)

def point_multiply(k, point):
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

def recover_public_key(message_hash, signature, recovery_id):
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
         0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    
    r = int.from_bytes(signature[:32], 'big')
    s = int.from_bytes(signature[32:64], 'big')
    
    if r >= n or s >= n:
        return None
    
    x = r + (recovery_id // 2) * n
    if x >= p:
        return None
    
    # Compute y coordinate
    alpha = (pow(x, 3, p) + 7) % p
    beta = pow(alpha, (p + 1) // 4, p)
    
    if beta % 2 != recovery_id % 2:
        beta = p - beta
    
    R = (x, beta)
    
    e = int.from_bytes(message_hash, 'big')
    r_inv = pow(r, n - 2, n)
    
    # Calculate public key point
    u1 = (-e * r_inv) % n
    u2 = (s * r_inv) % n
    
    point1 = point_multiply(u1, G)
    point2 = point_multiply(u2, R)
    
    return point_add(point1, point2)

def verify_signature():
    try:
        # Read input
        address = input().strip()
        message = input().strip()
        signature_b64 = input().strip()
        
        # Decode signature
        signature_bytes = base64.b64decode(signature_b64)
        
        if len(signature_bytes) != 65:
            print("INVALID")
            return
        
        recovery_id = signature_bytes[0] - 27
        if recovery_id < 0 or recovery_id > 3:
            print("INVALID")
            return
        
        signature = signature_bytes[1:]
        
        # Create message hash
        message_bytes = message.encode('utf-8')
        prefix = b'\x18Bitcoin Signed Message:\n'
        message_length = len(message_bytes).to_bytes((len(message_bytes).bit_length() + 7) // 8, 'big')
        if len(message_length) > 1 and message_length[0] == 0:
            message_length = message_length[1:]
        
        full_message = prefix + message_length + message_bytes
        message_hash = sha256(sha256(full_message))
        
        # Recover public key
        public_key_point = recover_public_key(message_hash, signature, recovery_id)
        
        if public_key_point is None:
            print("INVALID")
            return
        
        # Convert public key to address
        x, y = public_key_point
        public_key_bytes = b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
        
        # Create address
        public_key_hash = hash160(public_key_bytes)
        address_bytes = b'\x00' + public_key_hash
        checksum = sha256(sha256(address_bytes))[:4]
        full_address_bytes = address_bytes + checksum
        
        # Decode provided address for comparison
        try:
            decoded_address = base58_decode(address)
            if decoded_address == full_address_bytes:
                print("VALID")
            else:
                print("INVALID")
        except:
            print("INVALID")
    
    except:
        print("INVALID")

if __name__ == "__main__":
    verify_signature()