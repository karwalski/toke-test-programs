import sys

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def powmod(a, b, m):
    return pow(a, b, m)

def invmod(a, m):
    gcd, x, y = gcd_extended(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def solve_congruence(a, b, m):
    gcd, x, y = gcd_extended(a, m)
    if b % gcd != 0:
        return None
    
    # Reduce the equation
    a //= gcd
    b //= gcd
    m //= gcd
    
    # Find modular inverse of a mod m
    inv = invmod(a, m)
    if inv is None:
        return None
    
    return (b * inv) % m

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    
    if parts[0] == "powmod":
        a, b, m = int(parts[1]), int(parts[2]), int(parts[3])
        result = powmod(a, b, m)
        print(result)
    
    elif parts[0] == "invmod":
        a, m = int(parts[1]), int(parts[2])
        result = invmod(a, m)
        if result is None:
            print("NO SOLUTION")
        else:
            print(result)
    
    elif parts[0] == "congr":
        a, b, m = int(parts[1]), int(parts[2]), int(parts[3])
        result = solve_congruence(a, b, m)
        if result is None:
            print("NO SOLUTION")
        else:
            print(result)