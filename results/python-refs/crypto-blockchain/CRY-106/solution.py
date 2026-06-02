import hashlib

def base58_decode(s):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    base_count = len(alphabet)
    decoded = 0
    multi = 1
    
    for char in reversed(s):
        if char not in alphabet:
            return None
        decoded += multi * alphabet.index(char)
        multi *= base_count
    
    # Convert to bytes
    h = hex(decoded)[2:].rstrip('L')
    if len(h) % 2:
        h = '0' + h
    
    # Count leading zeros in original string
    leading_zeros = 0
    for c in s:
        if c == '1':
            leading_zeros += 1
        else:
            break
    
    # Add leading zero bytes
    result = bytes.fromhex(h)
    result = b'\x00' * leading_zeros + result
    
    return result

def validate_bitcoin_address(address):
    try:
        # Decode the address
        decoded = base58_decode(address)
        if decoded is None:
            return False, "Invalid Base58 encoding"
        
        # Bitcoin addresses should be 25 bytes when decoded
        if len(decoded) != 25:
            return False, "Invalid length"
        
        # Split into payload and checksum
        payload = decoded[:-4]
        checksum = decoded[-4:]
        
        # Calculate expected checksum
        hash1 = hashlib.sha256(payload).digest()
        hash2 = hashlib.sha256(hash1).digest()
        expected_checksum = hash2[:4]
        
        # Compare checksums
        if checksum == expected_checksum:
            return True, ""
        else:
            return False, "Checksum mismatch"
            
    except Exception as e:
        return False, str(e)

# Read input
address = input().strip()

# Validate
is_valid, reason = validate_bitcoin_address(address)

# Output result
if is_valid:
    print("VALID")
else:
    print(f"INVALID: {reason}")