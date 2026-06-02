import math

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def chinese_remainder_theorem(remainders, moduli):
    # Calculate M = LCM of all moduli
    M = moduli[0]
    for i in range(1, len(moduli)):
        M = lcm(M, moduli[i])
    
    x = 0
    for i in range(len(remainders)):
        Mi = M // moduli[i]
        gcd, yi, _ = extended_gcd(Mi, moduli[i])
        x += remainders[i] * Mi * yi
    
    return x % M, M

k = int(input())
remainders = []
moduli = []

for _ in range(k):
    a, n = map(int, input().split())
    remainders.append(a)
    moduli.append(n)

x, M = chinese_remainder_theorem(remainders, moduli)
print(f"x = {x} (mod {M})")