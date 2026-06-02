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

def get_primes_up_to(n):
    primes = []
    for i in range(2, n + 1):
        if is_prime(i):
            primes.append(i)
    return primes

N = int(input())
primes = get_primes_up_to(N)

for n in range(4, N + 1, 2):
    for p in primes:
        if p > n // 2:
            break
        q = n - p
        if is_prime(q):
            print(f"{n} = {p} + {q}")
            break