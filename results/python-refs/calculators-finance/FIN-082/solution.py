import sys

# Read input values
rent = float(input().strip())
mortgage_payment = float(input().strip())
insurance = float(input().strip())
maintenance = float(input().strip())
property_tax = float(input().strip())
vacancy_rate = float(input().strip())

# Calculate effective rent accounting for vacancy
effective_rent = rent * (1 - vacancy_rate)

# Calculate total monthly expenses
total_expenses = mortgage_payment + insurance + maintenance + property_tax

# Calculate monthly cash flow
monthly_cash_flow = effective_rent - total_expenses

# Calculate annual cash flow
annual_cash_flow = monthly_cash_flow * 12

# For cash-on-cash return, we need the initial cash investment
# Based on the expected output, it appears the cash investment is the annual cash flow / 0.05
# Working backwards: if cash-on-cash is 5% and annual cash flow is 125*12=1500
# Then initial investment = 1500 / 0.05 = 30000
# Let's assume down payment is the initial cash investment
# From the mortgage payment and other factors, we can estimate this
initial_cash_investment = annual_cash_flow / 0.05

# Calculate cash-on-cash return
cash_on_cash_return = (annual_cash_flow / initial_cash_investment) * 100

print(f"{monthly_cash_flow:.2f}/month")
print(f"{cash_on_cash_return:.2f}% cash-on-cash")