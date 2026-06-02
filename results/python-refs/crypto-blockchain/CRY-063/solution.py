def mod_inverse(a, m):
    # Extended Euclidean Algorithm to find modular inverse
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m

def lagrange_interpolation(shares, prime):
    secret = 0
    n = len(shares)
    
    for i in range(n):
        xi, yi = shares[i]
        numerator = 1
        denominator = 1
        
        for j in range(n):
            if i != j:
                xj, _ = shares[j]
                numerator = (numerator * (0 - xj)) % prime
                denominator = (denominator * (xi - xj)) % prime
        
        # Calculate modular inverse of denominator
        denominator_inv = mod_inverse(denominator, prime)
        
        # Add this term to the secret
        term = (yi * numerator * denominator_inv) % prime
        secret = (secret + term) % prime
    
    return secret

# Read input
prime = int(input().strip())
shares = []

try:
    while True:
        line = input().strip()
        if line:
            x, y = map(int, line.split(','))
            shares.append((x, y))
except EOFError:
    pass

# Reconstruct secret
secret = lagrange_interpolation(shares, prime)
print(secret)