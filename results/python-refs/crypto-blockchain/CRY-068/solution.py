import sys

def compact_to_target(compact_hex):
    # Convert hex string to integer
    compact = int(compact_hex, 16)
    
    # Extract exponent (first byte) and mantissa (last 3 bytes)
    exponent = (compact >> 24) & 0xFF
    mantissa = compact & 0xFFFFFF
    
    # Calculate the target
    if exponent <= 3:
        target = mantissa >> (8 * (3 - exponent))
    else:
        target = mantissa << (8 * (exponent - 3))
    
    # Format as 64-character hex string (32 bytes)
    return format(target, '064x')

# Read input from stdin
compact_input = input().strip()

# Convert and output
result = compact_to_target(compact_input)
print(result)