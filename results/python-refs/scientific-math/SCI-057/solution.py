import math
import sys
from collections import defaultdict

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    
    x = 2
    y = 2
    d = 1
    
    def f(x):
        return (x * x + 1) % n
    
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    
    return d if d != n else None

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def trial_division(n):
    factors = []
    
    # Check for factor 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check for odd factors
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    
    # If n is still > 1, then it's a prime
    if n > 1:
        factors.append(n)
    
    return factors

def factorize(n):
    if n == 1:
        return []
    
    factors = []
    
    def factorize_helper(num):
        if num == 1:
            return
        
        if is_prime(num):
            factors.append(num)
            return
        
        # Try trial division first for small factors
        temp_factors = trial_division(num)
        if len(temp_factors) > 1 or temp_factors[0] != num:
            factors.extend(temp_factors)
            return
        
        # Use Pollard's rho for larger composite numbers
        factor = pollard_rho(num)
        if factor and factor != num:
            factorize_helper(factor)
            factorize_helper(num // factor)
        else:
            factors.append(num)
    
    factorize_helper(n)
    return sorted(factors)

def format_output(n, factors):
    if n == 1:
        return "1 = 1"
    
    if not factors:
        return f"{n} = {n}"
    
    # Count occurrences of each prime
    prime_counts = defaultdict(int)
    for factor in factors:
        prime_counts[factor] += 1
    
    # Sort by prime value
    sorted_primes = sorted(prime_counts.keys())
    
    # Build output string
    terms = []
    for prime in sorted_primes:
        count = prime_counts[prime]
        if count == 1:
            terms.append(str(prime))
        else:
            terms.append(f"{prime}^{count}")
    
    return f"{n} = {' * '.join(terms)}"

def main():
    for line in sys.stdin:
        n = int(line.strip())
        factors = factorize(n)
        print(format_output(n, factors))

if __name__ == "__main__":
    main()