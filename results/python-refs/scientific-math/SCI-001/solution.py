n = int(input())

if n < 2:
    print()
    print("count: 0 primes")
else:
    # Create a boolean array "prime[0..n]" and initialize
    # all entries as true
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    
    p = 2
    while p * p <= n:
        # If prime[p] is not changed, then it is a prime
        if prime[p]:
            # Update all multiples of p
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    
    # Collect all prime numbers
    primes = []
    for i in range(2, n + 1):
        if prime[i]:
            primes.append(i)
    
    # Output the results
    if primes:
        print(' '.join(map(str, primes)))
    print(f"count: {len(primes)} primes")