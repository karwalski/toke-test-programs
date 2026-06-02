import sys

# Read input
line = input().strip()
target_amount, rate, periods = line.split()
target_amount = float(target_amount)
rate = float(rate)
periods = int(periods)

# Calculate sinking fund payment
# Formula: PMT = FV * (r / ((1 + r)^n - 1))
payment = target_amount * (rate / ((1 + rate) ** periods - 1))

# Output to 2 decimal places
print(f"{payment:.2f}")