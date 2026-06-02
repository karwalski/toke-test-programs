import sys

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def chinese_remainder_theorem(remainders, moduli):
    if not remainders:
        return 0
    
    result = remainders[0]
    modulus = moduli[0]
    
    for i in range(1, len(remainders)):
        a1, m1 = result, modulus
        a2, m2 = remainders[i], moduli[i]
        
        gcd, p, q = extended_gcd(m1, m2)
        
        if (a2 - a1) % gcd != 0:
            return None  # No solution exists
        
        lcm = m1 * m2 // gcd
        result = (a1 + m1 * ((a2 - a1) // gcd) * p) % lcm
        modulus = lcm
    
    return result

# Read input
remainders = []
moduli = []

for line in sys.stdin:
    line = line.strip()
    if line:
        remainder, mod = map(int, line.split())
        remainders.append(remainder)
        moduli.append(mod)

# Solve using CRT
solution = chinese_remainder_theorem(remainders, moduli)
print(solution)