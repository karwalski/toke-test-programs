p = int(input())
g = int(input())
a = int(input())
b = int(input())

# Alice's public key: g^a mod p
alice_public = pow(g, a, p)

# Bob's public key: g^b mod p
bob_public = pow(g, b, p)

# Shared secret: (g^b)^a mod p = (g^a)^b mod p
shared_secret = pow(bob_public, a, p)

print(alice_public)
print(bob_public)
print(shared_secret)