import sys
import math

def euler_totient(n):
    if n == 1:
        return 1
    
    result = n
    
    # Check for factor 2
    if n % 2 == 0:
        while n % 2 == 0:
            n //= 2
        result -= result // 2
    
    # Check for odd factors from 3 onwards
    i = 3
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 2
    
    # If n is still greater than 1, then it's a prime
    if n > 1:
        result -= result // n
    
    return result

for line in sys.stdin:
    n = int(line.strip())
    phi_n = euler_totient(n)
    print(f"phi({n}) = {phi_n}")