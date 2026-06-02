def base58_decode(s):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    base = len(alphabet)
    
    # Convert base58 to integer
    num = 0
    for char in s:
        num = num * base + alphabet.index(char)
    
    # Convert integer to bytes
    bytes_result = []
    while num > 0:
        bytes_result.append(num % 256)
        num //= 256
    
    # Handle leading zeros
    for char in s:
        if char == '1':
            bytes_result.append(0)
        else:
            break
    
    # Reverse to get correct byte order
    bytes_result.reverse()
    
    # Convert to hex
    return ''.join(f'{b:02x}' for b in bytes_result)

input_string = input().strip()
print(base58_decode(input_string))