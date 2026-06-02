import sys

def format_with_si(number, precision):
    if abs(number) >= 1e12:
        return f"{number / 1e12:.{precision}f}T"
    elif abs(number) >= 1e9:
        return f"{number / 1e9:.{precision}f}B"
    elif abs(number) >= 1e6:
        return f"{number / 1e6:.{precision}f}M"
    elif abs(number) >= 1e3:
        return f"{number / 1e3:.{precision}f}K"
    else:
        return f"{number:.{precision}f}"

def format_with_comma(number, precision):
    formatted = f"{number:.{precision}f}"
    parts = formatted.split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else ""
    
    # Add commas to integer part
    integer_with_commas = ""
    for i, digit in enumerate(reversed(integer_part)):
        if i > 0 and i % 3 == 0:
            integer_with_commas = "," + integer_with_commas
        integer_with_commas = digit + integer_with_commas
    
    if decimal_part and not all(c == '0' for c in decimal_part):
        return f"{integer_with_commas}.{decimal_part}"
    else:
        return integer_with_commas

def format_with_underscore(number, precision):
    formatted = f"{number:.{precision}f}"
    parts = formatted.split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else ""
    
    # Add underscores to integer part
    integer_with_underscores = ""
    for i, digit in enumerate(reversed(integer_part)):
        if i > 0 and i % 3 == 0:
            integer_with_underscores = "_" + integer_with_underscores
        integer_with_underscores = digit + integer_with_underscores
    
    if decimal_part and not all(c == '0' for c in decimal_part):
        return f"{integer_with_underscores}.{decimal_part}"
    else:
        return integer_with_underscores

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

mode = lines[0]
precision = int(lines[1])

# Process each number
for i in range(2, len(lines)):
    number = int(lines[i])
    
    if mode == "si":
        result = format_with_si(number, precision)
    elif mode == "comma":
        result = format_with_comma(number, precision)
    elif mode == "underscore":
        result = format_with_underscore(number, precision)
    
    print(result)