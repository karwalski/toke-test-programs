def add_large_integers(num1_str, num2_str):
    # Remove leading zeros and handle empty strings
    num1_str = num1_str.lstrip('0') or '0'
    num2_str = num2_str.lstrip('0') or '0'
    
    # Make strings same length by padding with zeros
    max_len = max(len(num1_str), len(num2_str))
    num1_str = num1_str.zfill(max_len)
    num2_str = num2_str.zfill(max_len)
    
    result = []
    carry = 0
    
    # Add from right to left
    for i in range(max_len - 1, -1, -1):
        digit_sum = int(num1_str[i]) + int(num2_str[i]) + carry
        result.append(str(digit_sum % 10))
        carry = digit_sum // 10
    
    # Add final carry if exists
    if carry:
        result.append(str(carry))
    
    # Reverse to get correct order
    result.reverse()
    
    return ''.join(result)

# Read input
num1 = input().strip()
num2 = input().strip()

# Calculate and print result
print(add_large_integers(num1, num2))