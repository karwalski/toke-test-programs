import sys

def base58_encode(data):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    # Convert bytes to integer
    num = int.from_bytes(data, 'big')
    
    # Handle zero case
    if num == 0:
        return alphabet[0]
    
    # Convert to base58
    encoded = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = alphabet[remainder] + encoded
    
    # Add leading '1's for each leading zero byte
    for byte in data:
        if byte == 0:
            encoded = alphabet[0] + encoded
        else:
            break
    
    return encoded

# Read hex string from stdin
hex_string = input().strip()

# Convert hex to bytes
byte_data = bytes.fromhex(hex_string)

# Encode to Base58
result = base58_encode(byte_data)

# Output result
print(result)