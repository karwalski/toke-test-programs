import math

# Read input
principal, rate, time = map(float, input().split())

# Calculate final value using continuously compounded formula: A = P * e^(rt)
final_value = principal * math.exp(rate * time)

# Output final value to 2 decimal places
print(f"{final_value:.2f}")