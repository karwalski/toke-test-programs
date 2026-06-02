import secrets
import sys

def is_prime(n, k=10):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Miller-Rabin test
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a prime number with specified bit length"""
    while True:
        # Generate random odd number with correct bit length
        n = secrets.randbits(bits)
        # Ensure it has the correct bit length
        n |= (1 << (bits - 1))  # Set MSB
        n |= 1  # Make it odd
        if is_prime(n):
            return n

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi):
    """Calculate modular inverse of e modulo phi"""
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

def generate_rsa_keypair(bit_size):
    """Generate RSA key pair"""
    # Generate two primes of half the bit size
    half_bits = bit_size // 2
    p = generate_prime(half_bits)
    q = generate_prime(half_bits)
    
    # Calculate n and phi(n)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Use standard e = 65537
    e = 65537
    
    # Calculate private exponent d
    d = mod_inverse(e, phi)
    
    return n, e, d

# Read bit size from stdin
bit_size = int(input().strip())

# Generate RSA key pair
n, e, d = generate_rsa_keypair(bit_size)

# Output in required format
print(f"n={n:x}")
print(f"e={e:x}")
print(f"d={d:x}")