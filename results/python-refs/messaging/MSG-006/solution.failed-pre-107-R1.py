import hashlib

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

class ECC:
    def __init__(self):
        # P-256 parameters
        self.p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        self.a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
        self.b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
        self.gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
        self.gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
        self.n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
        
    def point_add(self, px, py, qx, qy):
        if px is None:
            return qx, qy
        if qx is None:
            return px, py
            
        if px == qx:
            if py == qy:
                # Point doubling
                s = (3 * px * px + self.a) * mod_inverse(2 * py, self.p) % self.p
            else:
                return None, None  # Point at infinity
        else:
            s = (qy - py) * mod_inverse(qx - px, self.p) % self.p
            
        rx = (s * s - px - qx) % self.p
        ry = (s * (px - rx) - py) % self.p
        return rx, ry
    
    def point_multiply(self, k, px, py):
        if k == 0:
            return None, None
        if k == 1:
            return px, py
            
        result_x, result_y = None, None
        addend_x, addend_y = px, py
        
        while k:
            if k & 1:
                result_x, result_y = self.point_add(result_x, result_y, addend_x, addend_y)
            addend_x, addend_y = self.point_add(addend_x, addend_y, addend_x, addend_y)
            k >>= 1
            
        return result_x, result_y
    
    def generate_public_key(self, private_key):
        return self.point_multiply(private_key, self.gx, self.gy)
    
    def point_to_uncompressed_hex(self, px, py):
        return f"04{px:064x}{py:064x}"

def main():
    alice_private = int(input().strip(), 16)
    bob_private = int(input().strip(), 16)
    
    ecc = ECC()
    
    # Generate public keys
    alice_pub_x, alice_pub_y = ecc.generate_public_key(alice_private)
    bob_pub_x, bob_pub_y = ecc.generate_public_key(bob_private)
    
    # Convert to uncompressed hex format
    alice_pub_hex = ecc.point_to_uncompressed_hex(alice_pub_x, alice_pub_y)
    bob_pub_hex = ecc.point_to_uncompressed_hex(bob_pub_x, bob_pub_y)
    
    # Calculate shared secrets (should be the same)
    shared_x, shared_y = ecc.point_multiply(alice_private, bob_pub_x, bob_pub_y)
    shared_secret_hex = f"{shared_x:064x}"
    
    # Derive AES key using SHA-256
    shared_secret_bytes = bytes.fromhex(shared_secret_hex)
    aes_key = hashlib.sha256(shared_secret_bytes).hexdigest()
    
    print(alice_pub_hex)
    print(bob_pub_hex)
    print(shared_secret_hex)
    print(aes_key)

if __name__ == "__main__":
    main()