import sys

# Read input
investment_per_period = float(input().strip())
prices_line = input().strip()
prices = [float(p) for p in prices_line.split(',')]

# Calculate DCA investing
total_invested = 0
total_units = 0

for price in prices:
    total_invested += investment_per_period
    units_bought = investment_per_period / price
    total_units += units_bought

# Calculate average cost per unit
average_cost_per_unit = total_invested / total_units

# Output results
print(f"{total_invested:.2f}")
print(f"{total_units:.2f}")
print(f"{average_cost_per_unit:.2f}")