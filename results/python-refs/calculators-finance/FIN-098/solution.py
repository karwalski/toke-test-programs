n = int(input())

factors = []
d = 2

while d * d <= n:
    count = 0
    while n % d == 0:
        n //= d
        count += 1
    if count > 0:
        if count == 1:
            factors.append(str(d))
        else:
            factors.append(f"{d}^{count}")
    d += 1

if n > 1:
    factors.append(str(n))

print(" * ".join(factors))