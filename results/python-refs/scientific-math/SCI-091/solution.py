import sys

def convert_base(number_str, from_base, to_base):
    # Convert from source base to decimal
    decimal_value = 0
    for digit in number_str.upper():
        if digit.isdigit():
            digit_value = int(digit)
        else:
            digit_value = ord(digit) - ord('A') + 10
        decimal_value = decimal_value * from_base + digit_value
    
    # Convert from decimal to target base
    if decimal_value == 0:
        return "0"
    
    result = ""
    while decimal_value > 0:
        remainder = decimal_value % to_base
        if remainder < 10:
            result = str(remainder) + result
        else:
            result = chr(ord('A') + remainder - 10) + result
        decimal_value //= to_base
    
    return result

for line in sys.stdin:
    line = line.strip()
    if line:
        parts = line.split()
        number = parts[0]
        from_base = int(parts[1])
        to_base = int(parts[2])
        print(convert_base(number, from_base, to_base))