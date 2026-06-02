import sys

# Read source and target bases
source_base, target_base = map(int, input().split())

# Process each number
for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    
    # Convert from source base to decimal
    if source_base == 10:
        decimal_value = int(line)
    elif source_base == 2:
        decimal_value = int(line, 2)
    elif source_base == 8:
        decimal_value = int(line, 8)
    elif source_base == 16:
        decimal_value = int(line, 16)
    
    # Convert from decimal to target base
    if target_base == 10:
        result = str(decimal_value)
    elif target_base == 2:
        result = bin(decimal_value)[2:]
    elif target_base == 8:
        result = oct(decimal_value)[2:]
    elif target_base == 16:
        result = hex(decimal_value)[2:].upper()
    
    print(result)