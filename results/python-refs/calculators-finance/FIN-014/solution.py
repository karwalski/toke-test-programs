import sys

# Read input
discount_rate = float(input().strip())
cash_flows_line = input().strip()
cash_flows = [float(x) for x in cash_flows_line.split(',')]

# Calculate NPV
npv = 0
for i, cash_flow in enumerate(cash_flows):
    npv += cash_flow / ((1 + discount_rate) ** i)

# Output NPV rounded to 2 decimal places
print(f"{npv:.2f}")