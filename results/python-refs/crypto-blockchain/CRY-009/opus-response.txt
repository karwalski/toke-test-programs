import sys

def base58_encode(data):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    
    # Count leading zero bytes
    leading_zeros = 0
    for byte in data:
        if byte == 0:
            leading_zeros += 1
        else:
            break
    
    # Convert bytes to integer
    num = int.from_bytes(data, 'big')
    
    # Convert to base58
    encoded = ""
    while num > 0:
        num, remainder = divmod(num, 58)
        encoded = alphabet[remainder] + encoded
    
    # Add leading '1's for each leading zero byte
    encoded = alphabet[0] * leading_zeros + encoded
    
    if encoded == "":
        encoded = alphabet[0]
    
    return encoded

hex_string = input().strip()
byte_data = bytes.fromhex(hex_string)
result = base58_encode(byte_data)
print(result)