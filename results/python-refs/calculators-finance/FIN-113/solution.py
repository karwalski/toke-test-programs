import math

n, k, p = input().split()
n = int(n)
k = int(k)
p = float(p)

# Calculate binomial coefficient C(n,k) = n! / (k! * (n-k)!)
binomial_coeff = math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

# Calculate binomial probability P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
probability = binomial_coeff * (p ** k) * ((1 - p) ** (n - k))

print(f"{probability:.6f}")