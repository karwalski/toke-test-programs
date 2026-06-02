p = int(input())
g = int(input())
private_a = int(input())
private_b = int(input())

A = pow(g, private_a, p)
B = pow(g, private_b, p)
shared_secret = pow(B, private_a, p)

print(shared_secret)