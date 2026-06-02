def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

a, b = map(int, input().split())
gcd, x, y = extended_gcd(a, b)
print(gcd, x, y)