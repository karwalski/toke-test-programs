def get_proper_divisors(n):
    divisors = [1]
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i and n // i < n:
                divisors.append(n // i)
    return sorted(divisors)

def is_perfect(n):
    if n < 2:
        return False, []
    divisors = get_proper_divisors(n)
    if sum(divisors) == n:
        return True, divisors
    return False, []

N = int(input())

results = []
for num in range(2, N + 1):
    is_perf, divisors = is_perfect(num)
    if is_perf:
        divisor_str = "+".join(map(str, divisors))
        results.append(f"{num}: perfect (divisors: {divisor_str}={num})")

if results:
    print("\n".join(results))
else:
    print("(none in range)")