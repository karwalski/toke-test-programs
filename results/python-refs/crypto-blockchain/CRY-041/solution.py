import hashlib
import sys

def base58_encode(data):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    # Count leading zeros
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    # Convert to big integer
    num = int.from_bytes(data, 'big')
    
    # Convert to base58
    encoded = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = alphabet[remainder] + encoded
    
    # Add leading '1's for leading zeros
    encoded = '1' * leading_zeros + encoded
    
    return encoded

def hash160(data):
    sha256_hash = hashlib.sha256(data).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    return ripemd160_hash

def create_address(pubkey_hash):
    # Add version byte (0x00 for main network)
    versioned_payload = b'\x00' + pubkey_hash
    
    # Calculate checksum (first 4 bytes of double SHA256)
    checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
    
    # Combine payload and checksum
    address_bytes = versioned_payload + checksum
    
    # Encode with Base58
    return base58_encode(address_bytes)

# Read compressed public key from stdin
compressed_pubkey = input().strip()

# Convert hex to bytes
pubkey_bytes = bytes.fromhex(compressed_pubkey)

# Generate hash160 of the public key
pubkey_hash = hash160(pubkey_bytes)

# Create Bitcoin address
address = create_address(pubkey_hash)

print(address)