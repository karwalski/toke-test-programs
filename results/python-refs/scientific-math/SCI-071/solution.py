import random
import math

# Read input
a, b = map(float, input().split())
N = int(input())
coeffs = list(map(float, input().split()))

# Define polynomial function
def polynomial(x, coeffs):
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** i)
    return result

# Monte Carlo integration
samples = []
for _ in range(N):
    x = random.uniform(a, b)
    y = polynomial(x, coeffs)
    samples.append(y)

# Calculate estimate
estimate = (b - a) * sum(samples) / N

# Calculate variance
mean_y = sum(samples) / N
variance_y = sum((y - mean_y) ** 2 for y in samples) / N
variance_estimate = ((b - a) ** 2) * variance_y / N

# Calculate 95% confidence interval
std_error = math.sqrt(variance_estimate)
margin_error = 1.96 * std_error
ci_lower = estimate - margin_error
ci_upper = estimate + margin_error

# Output
print(f"Estimate: {estimate:.6f}")
print(f"Variance: {variance_estimate:.6f}")
print(f"95% CI: [{ci_lower:.6f}, {ci_upper:.6f}]")