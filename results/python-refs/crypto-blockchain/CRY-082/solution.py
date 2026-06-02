# Read input values
p = int(input())
g = int(input())
h = int(input())
v = int(input())
r = int(input())

# Calculate Pedersen commitment: C = g^v * h^r mod p
commitment = (pow(g, v, p) * pow(h, r, p)) % p

# Output the commitment value
print(commitment)