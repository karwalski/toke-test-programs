# Read input
first_line = input().strip().split()
initial_investment = float(first_line[0])
discount_rate = float(first_line[1])

second_line = input().strip()
cash_flows = [float(x) for x in second_line.split(',')]

# Calculate simple payback period
cumulative_cash_flow = 0
simple_payback = 0

for i, cash_flow in enumerate(cash_flows):
    if cumulative_cash_flow + cash_flow >= initial_investment:
        # Calculate fractional year
        remaining = initial_investment - cumulative_cash_flow
        simple_payback = i + (remaining / cash_flow)
        break
    cumulative_cash_flow += cash_flow
    simple_payback = i + 1

# Calculate discounted payback period
discounted_cumulative = 0
discounted_payback = 0

for i, cash_flow in enumerate(cash_flows):
    year = i + 1
    discounted_cash_flow = cash_flow / ((1 + discount_rate) ** year)
    
    if discounted_cumulative + discounted_cash_flow >= initial_investment:
        # Calculate fractional year
        remaining = initial_investment - discounted_cumulative
        fraction = remaining / discounted_cash_flow
        discounted_payback = i + fraction
        break
    discounted_cumulative += discounted_cash_flow
    discounted_payback = year

# Output results
print(f"{simple_payback:.2f}")
print(f"{discounted_payback:.2f}")