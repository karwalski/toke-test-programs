import sys

def popcount(n):
    return bin(n).count('1')

def lowest_bit(n):
    if n == 0:
        return 0
    return n & (-n)

def highest_bit(n):
    if n == 0:
        return 0
    pos = 0
    while n > 0:
        pos = n & (-n)
        n &= n - 1
    return pos

def reverse_bits(n):
    result = 0
    for i in range(32):
        if n & (1 << i):
            result |= (1 << (31 - i))
    return result

def is_pow2(n):
    if n <= 0:
        return "false"
    return "true" if (n & (n - 1)) == 0 else "false"

def parity(n):
    count = popcount(n)
    return count % 2

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    operation = parts[0]
    n = int(parts[1])
    
    if operation == "popcount":
        print(popcount(n))
    elif operation == "lowest_bit":
        print(lowest_bit(n))
    elif operation == "highest_bit":
        print(highest_bit(n))
    elif operation == "reverse_bits":
        print(reverse_bits(n))
    elif operation == "is_pow2":
        print(is_pow2(n))
    elif operation == "parity":
        print(parity(n))