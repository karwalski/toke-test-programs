import hashlib
import hmac
import sys

def pbkdf2_hmac_sha512(password, salt, iterations=2048):
    """PBKDF2 implementation using HMAC-SHA512"""
    dklen = 64
    password = password.encode('utf-8')
    
    def prf(data):
        return hmac.new(password, data, hashlib.sha512).digest()
    
    key = b''
    i = 1
    while len(key) < dklen:
        u = prf(salt + i.to_bytes(4, 'big'))
        f = u
        for _ in range(iterations - 1):
            u = prf(u)
            f = bytes(a ^ b for a, b in zip(f, u))
        key += f
        i += 1
    
    return key[:dklen]

def hmac_sha512(key, data):
    """HMAC-SHA512"""
    return hmac.new(key, data, hashlib.sha512).digest()

def secp256k1_point_add(p1, p2):
    """Point addition on secp256k1"""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    
    P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2:
        if y1 == y2:
            # Point doubling
            s = (3 * x1 * x1 * pow(2 * y1, P - 2, P)) % P
        else:
            return None  # Point at infinity
    else:
        s = ((y2 - y1) * pow(x2 - x1, P - 2, P)) % P
    
    x3 = (s * s - x1 - x2) % P
    y3 = (s * (x1 - x3) - y1) % P
    
    return (x3, y3)

def secp256k1_multiply(k, point=None):
    """Scalar multiplication on secp256k1"""
    if point is None:
        # Generator point
        point = (
            0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        )
    
    if k == 0:
        return None
    
    result = None
    addend = point
    
    while k:
        if k & 1:
            result = secp256k1_point_add(result, addend)
        addend = secp256k1_point_add(addend, addend)
        k >>= 1
    
    return result

def derive_key(parent_key, parent_chain, index):
    """Derive child key using BIP32"""
    if index >= 0x80000000:  # Hardened derivation
        data = b'\x00' + parent_key + index.to_bytes(4, 'big')
    else:  # Non-hardened derivation
        # Get public key from private key
        point = secp256k1_multiply(int.from_bytes(parent_key, 'big'))
        if point is None:
            raise ValueError("Invalid private key")
        
        x, y = point
        if y % 2 == 0:
            pub_key = b'\x02' + x.to_bytes(32, 'big')
        else:
            pub_key = b'\x03' + x.to_bytes(32, 'big')
        
        data = pub_key + index.to_bytes(4, 'big')
    
    mac = hmac_sha512(parent_chain, data)
    child_key = mac[:32]
    child_chain = mac[32:]
    
    if index < 0x80000000:  # Non-hardened, need to add to parent key
        parent_int = int.from_bytes(parent_key, 'big')
        child_int = int.from_bytes(child_key, 'big')
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        final_key = ((parent_int + child_int) % n).to_bytes(32, 'big')
    else:
        final_key = child_key
    
    return final_key, child_chain

def base58_encode(data):
    """Base58 encoding"""
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    # Count leading zeros
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    # Convert to integer
    num = int.from_bytes(data, 'big')
    
    # Convert to base58
    result = []
    while num > 0:
        num, remainder = divmod(num, 58)
        result.append(alphabet[remainder])
    
    # Add leading 1s for leading zeros
    result.extend(['1'] * leading_zeros)
    
    return ''.join(reversed(result))

def private_key_to_address(private_key):
    """Convert private key to Bitcoin address"""
    # Get public key
    point = secp256k1_multiply(int.from_bytes(private_key, 'big'))
    if point is None:
        raise ValueError("Invalid private key")
    
    x, y = point
    if y % 2 == 0:
        pub_key = b'\x02' + x.to_bytes(32, 'big')
    else:
        pub_key = b'\x03' + x.to_bytes(32, 'big')
    
    # Hash public key
    sha256_hash = hashlib.sha256(pub_key).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    
    # Add version byte for mainnet
    versioned_hash = b'\x00' + ripemd160_hash
    
    # Double SHA256 for checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
    
    # Final address
    address_bytes = versioned_hash + checksum
    return base58_encode(address_bytes)

def main():
    # Read mnemonic from stdin
    mnemonic = input().strip()
    
    # Convert mnemonic to seed
    seed = pbkdf2_hmac_sha512(mnemonic, b'mnemonic')
    
    # Master key derivation
    master_mac = hmac_sha512(b'Bitcoin seed', seed)
    master_key = master_mac[:32]
    master_chain = master_mac[32:]
    
    # Derive m/44'/0'/0'/0
    # m/44'
    key, chain = derive_key(master_key, master_chain, 44 + 0x80000000)
    # m/44'/0'
    key, chain = derive_key(key, chain, 0 + 0x80000000)
    # m/44'/0'/0'
    key, chain = derive_key(key, chain, 0 + 0x80000000)
    # m/44'/0'/0'/0
    key, chain = derive_key(key, chain, 0)
    
    # Generate first 5 addresses
    for i in range(5):
        child_key, _ = derive_key(key, chain, i)
        address = private_key_to_address(child_key)
        print(f"m/44'/0'/0'/0/{i}: {address}")

if __name__ == "__main__":
    main()