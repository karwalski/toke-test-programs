import sys

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % m + m) % m

def lagrange_interpolation(shares, prime):
    # Reconstruct the secret using Lagrange interpolation at x=0
    result = 0
    n = len(shares)
    
    for i in range(n):
        xi, yi = shares[i]
        
        # Calculate Lagrange basis polynomial at x=0
        numerator = 1
        denominator = 1
        
        for j in range(n):
            if i != j:
                xj, _ = shares[j]
                numerator = (numerator * (-xj)) % prime
                denominator = (denominator * (xi - xj)) % prime
        
        # Calculate yi * (numerator / denominator) mod prime
        denominator_inv = mod_inverse(denominator, prime)
        term = (yi * numerator * denominator_inv) % prime
        result = (result + term) % prime
    
    return result

def reconstruct_secret(threshold, shares):
    # Use a large prime for field arithmetic
    # This should be larger than any possible secret value
    prime = 2**127 - 1  # Mersenne prime
    
    if len(shares) < threshold:
        return "ERROR"
    
    # Use only the first 'threshold' shares
    shares = shares[:threshold]
    
    try:
        # Convert hex shares to integers
        int_shares = []
        for idx, hex_val in shares:
            int_shares.append((idx, int(hex_val, 16)))
        
        # Reconstruct the secret
        secret = lagrange_interpolation(int_shares, prime)
        
        # Convert back to hex
        hex_secret = hex(secret)[2:]  # Remove '0x' prefix
        
        return f"reconstructed: {hex_secret}"
    
    except Exception:
        return "ERROR"

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if not lines:
        print("ERROR")
        return
    
    try:
        threshold = int(lines[0])
        shares = []
        
        for i in range(1, len(lines)):
            parts = lines[i].split()
            if len(parts) != 2:
                continue
            share_index = int(parts[0])
            hex_share = parts[1]
            shares.append((share_index, hex_share))
        
        result = reconstruct_secret(threshold, shares)
        print(result)
    
    except Exception:
        print("ERROR")

if __name__ == "__main__":
    main()