import hashlib
import sys

def base58_encode(data):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    # Convert to integer
    num = int.from_bytes(data, 'big')
    
    # Count leading zeros
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    # Convert to base58
    result = ''
    while num > 0:
        num, remainder = divmod(num, 58)
        result = alphabet[remainder] + result
    
    # Add leading '1's for leading zeros
    result = '1' * leading_zeros + result
    
    return result

def hex_to_wif(hex_key):
    # Convert hex to bytes
    private_key = bytes.fromhex(hex_key)
    
    # Add mainnet prefix (0x80)
    extended_key = b'\x80' + private_key
    
    # Double SHA256 for checksum
    hash1 = hashlib.sha256(extended_key).digest()
    hash2 = hashlib.sha256(hash1).digest()
    checksum = hash2[:4]
    
    # Combine and encode
    final_key = extended_key + checksum
    wif = base58_encode(final_key)
    
    return wif

# Read input
hex_key = input().strip()

# Convert and output
wif = hex_to_wif(hex_key)
print(wif)