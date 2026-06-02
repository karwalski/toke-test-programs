def sieve_of_sundaram(n):
    # Calculate k for the Sieve of Sundaram
    k = (n - 1) // 2
    
    # Create a boolean array and initialize all entries as True
    marked = [False] * (k + 1)
    
    # Mark numbers that are not prime using Sundaram's formula
    for i in range(1, k + 1):
        j = i
        while i + j + 2 * i * j <= k:
            marked[i + j + 2 * i * j] = True
            j += 1
    
    # Collect primes
    primes = []
    
    # 2 is the only even prime
    if n >= 2:
        primes.append(2)
    
    # Other primes are of the form 2*i + 1
    for i in range(1, k + 1):
        if not marked[i]:
            prime = 2 * i + 1
            if prime <= n:
                primes.append(prime)
    
    return primes

# Read input
n = int(input())

# Find primes using Sieve of Sundaram
primes = sieve_of_sundaram(n)

# Output results
print(' '.join(map(str, primes)))
print(f"count: {len(primes)} primes")