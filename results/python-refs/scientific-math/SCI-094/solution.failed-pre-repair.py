def get_proper_divisors(n):
    """Get all proper divisors of n (divisors less than n)"""
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != 1 and i != n // i and n // i < n:
                divisors.append(n // i)
    return sorted(divisors)

def is_perfect(n):
    """Check if n is a perfect number and return divisors if it is"""
    divisors = get_proper_divisors(n)
    if sum(divisors) == n:
        return True, divisors
    return False, []

# Read input
N = int(input())

# Find and verify perfect numbers up to N
for num in range(1, N + 1):
    is_perf, divisors = is_perfect(num)
    if is_perf:
        divisor_str = "+".join(map(str, divisors))
        print(f"{num}: perfect (divisors: {divisor_str}={num})")