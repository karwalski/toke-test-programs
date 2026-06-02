def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

N = int(input())
count = 0

for p in range(2, N - 1):
    if is_prime(p) and is_prime(p + 2):
        print(f"({p},{p+2})")
        count += 1

print(f"count: {count} pairs.")