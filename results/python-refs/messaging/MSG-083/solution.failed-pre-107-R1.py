import secrets
import sys

def mod_inverse(a, m):
    """Calculate modular inverse using extended Euclidean algorithm"""
    if m == 1:
        return 0
    
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
    """Reconstruct secret using Lagrange interpolation"""
    x_values = [share[0] for share in shares]
    y_values = [share[1] for share in shares]
    
    result = 0
    for i in range(len(shares)):
        xi, yi = x_values[i], y_values[i]
        
        # Calculate Lagrange basis polynomial
        numerator = 1
        denominator = 1
        
        for j in range(len(shares)):
            if i != j:
                xj = x_values[j]
                numerator = (numerator * (0 - xj)) % prime
                denominator = (denominator * (xi - xj)) % prime
        
        # Calculate yi * Li(0)
        lagrange_coeff = (numerator * mod_inverse(denominator, prime)) % prime
        result = (result + yi * lagrange_coeff) % prime
    
    return result

def shamir_secret_sharing(secret_bytes, n, k):
    """Split secret into n shares with threshold k"""
    # Use a large prime (256-bit)
    prime = 2**256 - 189
    
    # Convert secret bytes to integer
    secret = int.from_bytes(secret_bytes, 'big')
    
    # Generate random coefficients for polynomial
    coefficients = [secret]
    for _ in range(k - 1):
        coefficients.append(secrets.randbelow(prime))
    
    # Generate shares
    shares = []
    for x in range(1, n + 1):
        y = 0
        for i, coeff in enumerate(coefficients):
            y = (y + coeff * pow(x, i, prime)) % prime
        shares.append((x, y))
    
    return shares, prime

def int_to_hex_bytes(value, byte_length):
    """Convert integer to hex string with proper padding"""
    hex_str = hex(value)[2:]  # Remove '0x' prefix
    if len(hex_str) % 2:
        hex_str = '0' + hex_str
    
    # Pad to desired byte length
    target_hex_length = byte_length * 2
    if len(hex_str) < target_hex_length:
        hex_str = '0' * (target_hex_length - len(hex_str)) + hex_str
    
    return hex_str

def main():
    # Read input
    secret_hex = input().strip()
    n = int(input().strip())
    k = int(input().strip())
    
    # Convert hex secret to bytes
    secret_bytes = bytes.fromhex(secret_hex)
    
    # Generate shares
    shares, prime = shamir_secret_sharing(secret_bytes, n, k)
    
    # Output shares
    for i, (x, y) in enumerate(shares, 1):
        # Convert share to hex format
        # Each share consists of x coordinate (1 byte) and y coordinate (variable length)
        x_hex = format(x, '02x')
        y_hex = int_to_hex_bytes(y, len(secret_bytes) + 4)  # Add some padding for safety
        share_hex = x_hex + y_hex
        
        print(f"share {i}: {share_hex}")
    
    print(f"reconstruction requires any {k} of {n} shares")

if __name__ == "__main__":
    main()