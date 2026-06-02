import sys
import math

def sieve_of_atkin(n):
    if n < 2:
        return []
    
    # Initialize the sieve
    sieve = [False] * (n + 1)
    
    # Put in candidate primes:
    # integers which have an odd number of representations by certain quadratic forms
    for x in range(1, int(math.sqrt(n)) + 1):
        for y in range(1, int(math.sqrt(n)) + 1):
            # Main part of Sieve of Atkin
            # First quadratic using m = 4x^2 + y^2
            m = 4 * x * x + y * y
            if m <= n and (m % 12 == 1 or m % 12 == 5):
                sieve[m] = not sieve[m]
            
            # Second quadratic using m = 3x^2 + y^2
            m = 3 * x * x + y * y
            if m <= n and m % 12 == 7:
                sieve[m] = not sieve[m]
            
            # Third quadratic using m = 3x^2 - y^2
            if x > y:
                m = 3 * x * x - y * y
                if m <= n and m % 12 == 11:
                    sieve[m] = not sieve[m]
    
    # Mark all multiples of squares as non-prime
    for i in range(5, int(math.sqrt(n)) + 1):
        if sieve[i]:
            k = i * i
            while k <= n:
                sieve[k] = False
                k += i * i
    
    # Collect primes
    primes = []
    if n >= 2:
        primes.append(2)
    if n >= 3:
        primes.append(3)
    
    for i in range(5, n + 1):
        if sieve[i]:
            primes.append(i)
    
    return primes

# Read input
n = int(input().strip())

# Find primes using Sieve of Atkin
primes = sieve_of_atkin(n)

# Output results
if primes:
    print(' '.join(map(str, primes)))
print(f"count: {len(primes)} primes")