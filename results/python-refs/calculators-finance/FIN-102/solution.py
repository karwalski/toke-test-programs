def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

a, m = map(int, input().split())
result = mod_inverse(a, m)
if result is None:
    print("NO_INVERSE")
else:
    print(result)