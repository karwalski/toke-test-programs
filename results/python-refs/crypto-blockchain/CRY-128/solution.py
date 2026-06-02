import re
import hashlib
import sys

def base58_decode(s):
    """Decode Base58 string, returns bytes"""
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    base_count = len(alphabet)
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        if char not in alphabet:
            return None
        decoded += multi * alphabet.index(char)
        multi *= base_count
    
    # Convert to bytes
    h = hex(decoded)[2:]
    if len(h) % 2:
        h = '0' + h
    
    try:
        result = bytes.fromhex(h)
    except:
        return None
    
    # Add leading zeros
    pad = 0
    for c in s[::-1]:
        if c == alphabet[0]:
            pad += 1
        else:
            break
    
    return b'\x00' * pad + result

def validate_bitcoin_address(address):
    """Validate Bitcoin address format and checksum"""
    try:
        # Must be 25-34 characters
        if len(address) < 25 or len(address) > 34:
            return False, "Invalid length"
        
        # Must start with 1 or 3
        if not (address.startswith('1') or address.startswith('3')):
            return False, "Invalid prefix"
        
        # Decode base58
        decoded = base58_decode(address)
        if decoded is None:
            return False, "Invalid base58 encoding"
        
        # Should be exactly 25 bytes
        if len(decoded) != 25:
            return False, "Invalid decoded length"
        
        # Check checksum
        payload = decoded[:-4]
        checksum = decoded[-4:]
        hash_result = hashlib.sha256(hashlib.sha256(payload).digest()).digest()
        if hash_result[:4] != checksum:
            return False, "Invalid checksum"
        
        return True, ""
    except:
        return False, "Invalid format"

def validate_ethereum_address(address):
    """Validate Ethereum address format"""
    # Must start with 0x and be 42 characters total
    if not address.startswith('0x') or len(address) != 42:
        return False, "Invalid format"
    
    # Check if all characters after 0x are valid hex
    hex_part = address[2:]
    if not re.match('^[0-9a-fA-F]+$', hex_part):
        return False, "Invalid hex characters"
    
    return True, ""

def detect_and_validate_address(address):
    """Detect blockchain and validate address"""
    address = address.strip()
    
    # Check Bitcoin patterns
    if re.match('^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        valid, reason = validate_bitcoin_address(address)
        if valid:
            return "Bitcoin", "VALID"
        else:
            return "Bitcoin", f"INVALID: {reason}"
    
    # Check Ethereum pattern
    elif re.match('^0x[0-9a-fA-F]{40}$', address):
        valid, reason = validate_ethereum_address(address)
        if valid:
            return "Ethereum", "VALID"
        else:
            return "Ethereum", f"INVALID: {reason}"
    
    # Unknown format
    else:
        return "Unknown", "INVALID: Unrecognized format"

# Read input
address = input().strip()

# Detect and validate
chain, status = detect_and_validate_address(address)

# Output
print(chain)
print(status)