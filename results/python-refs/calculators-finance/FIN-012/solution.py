import sys
import math

# Read input from stdin
line = input().strip()
loan_amount, annual_rate, years = line.split()

loan_amount = float(loan_amount)
annual_rate = float(annual_rate)
years = int(years)

# Calculate monthly payment using standard mortgage formula
monthly_rate = annual_rate / 12
num_payments = years * 12

if monthly_rate == 0:
    monthly_payment = loan_amount / num_payments
else:
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)

# Round to 2 decimal places and print
print(f"{monthly_payment:.2f}")