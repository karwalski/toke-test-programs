import sys

def mobius(n):
    if n == 1:
        return 1
    
    # Find prime factorization
    factors = {}
    temp = n
    d = 2
    
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    
    # Check if any prime has power > 1
    for power in factors.values():
        if power > 1:
            return 0
    
    # Return (-1)^k where k is number of distinct prime factors
    return (-1) ** len(factors)

for line in sys.stdin:
    n = int(line.strip())
    result = mobius(n)
    print(f"mu({n}) = {result}")