import hashlib
import hmac

def base58_encode(data):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int.from_bytes(data, 'big')
    encoded = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = alphabet[remainder] + encoded
    
    # Handle leading zeros
    for byte in data:
        if byte == 0:
            encoded = '1' + encoded
        else:
            break
    
    return encoded

def hash160(data):
    sha256_hash = hashlib.sha256(data).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    return ripemd160_hash

def create_address(pubkey_hash):
    # Add version byte (0x00 for mainnet)
    versioned_payload = b'\x00' + pubkey_hash
    
    # Calculate checksum
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    
    # Combine and encode
    full_payload = versioned_payload + checksum
    return base58_encode(full_payload)

def point_add(p1, p2):
    # Secp256k1 parameters
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2:
        if y1 == y2:
            # Point doubling
            s = (3 * x1 * x1 * pow(2 * y1, p - 2, p)) % p
            x3 = (s * s - 2 * x1) % p
            y3 = (s * (x1 - x3) - y1) % p
            return (x3, y3)
        else:
            return None  # Point at infinity
    else:
        # Point addition
        s = ((y2 - y1) * pow(x2 - x1, p - 2, p)) % p
        x3 = (s * s - x1 - x2) % p
        y3 = (s * (x1 - x3) - y1) % p
        return (x3, y3)

def point_multiply(k, point):
    # Secp256k1 generator point
    if point is None or k == 0:
        return None
    
    result = None
    addend = point
    
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    
    return result

def derive_child_key(parent_pubkey, chain_code, index):
    # For public key derivation (non-hardened)
    parent_pubkey_bytes = bytes.fromhex(parent_pubkey)
    chain_code_bytes = bytes.fromhex(chain_code)
    
    # Create the data for HMAC
    index_bytes = index.to_bytes(4, 'big')
    data = parent_pubkey_bytes + index_bytes
    
    # Calculate HMAC-SHA512
    hmac_result = hmac.new(chain_code_bytes, data, hashlib.sha512).digest()
    
    # Split the result
    child_key = hmac_result[:32]
    child_chain_code = hmac_result[32:]
    
    # Convert parent public key to point
    parent_x = int.from_bytes(parent_pubkey_bytes[1:33], 'big')
    parent_y_squared = (pow(parent_x, 3, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F) + 7) % 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    parent_y = pow(parent_y_squared, (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F + 1) // 4, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)
    
    # Check if y coordinate matches the compressed format
    if parent_pubkey_bytes[0] == 0x03 and parent_y % 2 == 0:
        parent_y = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F - parent_y
    elif parent_pubkey_bytes[0] == 0x02 and parent_y % 2 == 1:
        parent_y = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F - parent_y
    
    parent_point = (parent_x, parent_y)
    
    # Generator point for secp256k1
    gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    generator = (gx, gy)
    
    # Calculate child public key point
    child_key_int = int.from_bytes(child_key, 'big')
    child_point_addition = point_multiply(child_key_int, generator)
    child_point = point_add(parent_point, child_point_addition)
    
    if child_point is None:
        return None, None
    
    # Convert back to compressed public key format
    x, y = child_point
    if y % 2 == 0:
        child_pubkey = '02' + x.to_bytes(32, 'big').hex()
    else:
        child_pubkey = '03' + x.to_bytes(32, 'big').hex()
    
    return child_pubkey, child_chain_code.hex()

def main():
    # Read input
    master_pubkey = input().strip()
    chain_code = input().strip()
    n = int(input().strip())
    
    # Current derivation state
    current_pubkey = master_pubkey
    current_chain_code = chain_code
    
    # Generate addresses
    for i in range(n):
        # Derive child key for index i
        child_pubkey, child_chain_code = derive_child_key(current_pubkey, current_chain_code, i)
        
        if child_pubkey is None:
            print(f"{i}: ERROR")
            continue
        
        # Convert public key to address
        pubkey_bytes = bytes.fromhex(child_pubkey)
        pubkey_hash = hash160(pubkey_bytes)
        address = create_address(pubkey_hash)
        
        print(f"{i}: {address}")

if __name__ == "__main__":
    main()