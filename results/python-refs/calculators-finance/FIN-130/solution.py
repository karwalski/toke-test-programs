import sys
import math

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse weights
weights = [float(x) for x in lines[0].split(',')]

# Parse variances
variances = [float(x) for x in lines[1].split(',')]

# Parse correlation matrix
n = len(weights)
correlation_matrix = []
for i in range(2, 2 + n):
    row = [float(x) for x in lines[i].split()]
    correlation_matrix.append(row)

# Calculate portfolio variance
portfolio_variance = 0.0

# Add variance terms (diagonal elements)
for i in range(n):
    portfolio_variance += weights[i] * weights[i] * variances[i]

# Add covariance terms (off-diagonal elements)
for i in range(n):
    for j in range(n):
        if i != j:
            covariance = correlation_matrix[i][j] * math.sqrt(variances[i]) * math.sqrt(variances[j])
            portfolio_variance += weights[i] * weights[j] * covariance

# Calculate portfolio standard deviation
portfolio_std = math.sqrt(portfolio_variance)

# Output results
print(f"{portfolio_variance:.6f}")
print(f"{portfolio_std:.6f}")