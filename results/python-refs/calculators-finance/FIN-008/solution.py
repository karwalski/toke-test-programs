import re
import sys

def parse_complex(s):
    # Handle cases like "3+4i", "3-4i", "3", "4i", "-3+4i", etc.
    s = s.replace(' ', '')
    
    # Handle pure imaginary numbers like "4i" or "-4i"
    if s.endswith('i') and ('+' not in s[1:] and '-' not in s[1:]):
        if s == 'i':
            return complex(0, 1)
        elif s == '-i':
            return complex(0, -1)
        else:
            return complex(0, float(s[:-1]))
    
    # Handle real numbers
    if 'i' not in s:
        return complex(float(s), 0)
    
    # Handle complex numbers with both real and imaginary parts
    if '+' in s[1:]:  # positive imaginary part
        parts = s.split('+')
        real = float(parts[0])
        imag_str = parts[1][:-1]  # remove 'i'
        if imag_str == '':
            imag = 1
        else:
            imag = float(imag_str)
        return complex(real, imag)
    elif '-' in s[1:]:  # negative imaginary part
        # Find the last minus sign
        minus_pos = s.rfind('-')
        real = float(s[:minus_pos])
        imag_str = s[minus_pos+1:-1]  # remove 'i'
        if imag_str == '':
            imag = -1
        else:
            imag = -float(imag_str)
        return complex(real, imag)
    
    return complex(0, 0)

def format_complex(c):
    real = c.real
    imag = c.imag
    
    # Handle rounding to avoid floating point precision issues
    if abs(real - round(real)) < 1e-10:
        real = round(real)
    if abs(imag - round(imag)) < 1e-10:
        imag = round(imag)
    
    if real == 0 and imag == 0:
        return "0"
    elif real == 0:
        if imag == 1:
            return "i"
        elif imag == -1:
            return "-i"
        else:
            return f"{int(imag) if imag == int(imag) else imag}i"
    elif imag == 0:
        return str(int(real) if real == int(real) else real)
    else:
        real_str = str(int(real) if real == int(real) else real)
        if imag == 1:
            return f"{real_str}+i"
        elif imag == -1:
            return f"{real_str}-i"
        elif imag > 0:
            imag_str = str(int(imag) if imag == int(imag) else imag)
            return f"{real_str}+{imag_str}i"
        else:
            imag_str = str(int(-imag) if -imag == int(-imag) else -imag)
            return f"{real_str}-{imag_str}i"

# Read input
line = input().strip()

# Parse the input to extract the two complex numbers and operator
# Split by operators, being careful about minus signs
operators = ['+', '-', '*', '/']
op_pos = -1
op = ''

for i in range(1, len(line)):  # Start from 1 to avoid initial minus sign
    if line[i] in operators and not (line[i-1] in 'i0123456789'):
        # Look ahead to see if this is really an operator
        # and not part of a complex number
        remaining = line[i+1:].strip()
        if remaining and remaining[0] not in operators:
            op_pos = i
            op = line[i]
            break

if op_pos == -1:
    # Try a different approach - look for operator after 'i' or digit
    for i in range(len(line)):
        if line[i] in operators:
            # Check if previous character suggests end of first number
            if i > 0 and (line[i-1] == 'i' or line[i-1].isdigit()):
                op_pos = i
                op = line[i]
                break

num1_str = line[:op_pos].strip()
num2_str = line[op_pos+1:].strip()

num1 = parse_complex(num1_str)
num2 = parse_complex(num2_str)

# Perform the operation
if op == '+':
    result = num1 + num2
elif op == '-':
    result = num1 - num2
elif op == '*':
    result = num1 * num2
elif op == '/':
    result = num1 / num2

# Format and print the result
print(format_complex(result))