def convert_base(number, source_base, target_base):
    # Convert from source base to decimal
    decimal_value = 0
    number = number.upper()
    
    for i, digit in enumerate(reversed(number)):
        if digit.isdigit():
            digit_value = int(digit)
        else:
            digit_value = ord(digit) - ord('A') + 10
        decimal_value += digit_value * (source_base ** i)
    
    # Convert from decimal to target base
    if decimal_value == 0:
        return "0"
    
    result = ""
    while decimal_value > 0:
        remainder = decimal_value % target_base
        if remainder < 10:
            result = str(remainder) + result
        else:
            result = chr(ord('A') + remainder - 10) + result
        decimal_value //= target_base
    
    return result

# Read input
line = input().strip()
parts = line.split()
number = parts[0]
source_base = int(parts[1])
target_base = int(parts[2])

# Convert and print result
result = convert_base(number, source_base, target_base)
print(result)