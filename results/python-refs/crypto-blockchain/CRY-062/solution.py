import random

def shamir_secret_sharing(secret, threshold, num_shares):
    # Generate random coefficients for polynomial of degree (threshold - 1)
    coefficients = [secret]  # a0 = secret
    for _ in range(threshold - 1):
        coefficients.append(random.randint(1, 2**31 - 1))
    
    # Generate shares by evaluating polynomial at x = 1, 2, ..., num_shares
    shares = []
    for x in range(1, num_shares + 1):
        y = 0
        for i, coeff in enumerate(coefficients):
            y += coeff * (x ** i)
        shares.append((x, y))
    
    return shares

# Read input
secret = int(input().strip())
threshold = int(input().strip())
num_shares = int(input().strip())

# Generate shares
shares = shamir_secret_sharing(secret, threshold, num_shares)

# Output shares
for x, y in shares:
    print(f"{x},{y}")