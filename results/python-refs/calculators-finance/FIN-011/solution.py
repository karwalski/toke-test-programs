import math

# Read input
principal, rate, frequency, years = map(float, input().split())

# Calculate compound interest using the formula: A = P(1 + r/n)^(nt)
amount = principal * (1 + rate / frequency) ** (frequency * years)

# Round to 2 decimal places and print
print(f"{amount:.2f}")