# Read input
line = input().strip()
revenue, cogs, operating_expenses, taxes = map(int, line.split())

# Calculate margins
gross_profit = revenue - cogs
gross_margin = (gross_profit / revenue) * 100

operating_profit = gross_profit - operating_expenses
operating_margin = (operating_profit / revenue) * 100

net_profit = operating_profit - taxes
net_margin = (net_profit / revenue) * 100

# Output results
print(f"{gross_margin:.2f}%")
print(f"{operating_margin:.2f}%")
print(f"{net_margin:.2f}%")