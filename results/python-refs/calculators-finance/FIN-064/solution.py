import sys
import math

# Read input
risk_free_rate = float(input().strip())
returns_line = input().strip()
returns = [float(x) for x in returns_line.split(',')]

# Calculate mean return
mean_return = sum(returns) / len(returns)

# Calculate standard deviation
variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
std_dev = math.sqrt(variance)

# Calculate Sharpe ratio
sharpe_ratio = (mean_return - risk_free_rate) / std_dev

# Output to 4 decimal places
print(f"{sharpe_ratio:.4f}")