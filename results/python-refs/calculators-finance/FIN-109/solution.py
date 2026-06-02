# Read input
line = input().strip()
equity_weight, debt_weight, cost_equity, cost_debt, tax_rate = map(float, line.split())

# Calculate WACC
# WACC = (E/V * Re) + (D/V * Rd * (1 - Tc))
# where E/V = equity_weight, D/V = debt_weight, Re = cost_equity, Rd = cost_debt, Tc = tax_rate
wacc = (equity_weight * cost_equity) + (debt_weight * cost_debt * (1 - tax_rate))

# Convert to percentage and format to 2 decimal places
wacc_percentage = wacc * 100
print(f"{wacc_percentage:.2f}%")