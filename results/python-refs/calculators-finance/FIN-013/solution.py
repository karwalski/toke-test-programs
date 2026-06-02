import sys
import math

# Read input
line = input().strip()
loan_amount, annual_rate, months = line.split()
loan_amount = float(loan_amount)
annual_rate = float(annual_rate)
months = int(months)

# Calculate monthly payment
monthly_rate = annual_rate / 12
payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)

# Generate amortization schedule
balance = loan_amount
for period in range(1, months + 1):
    interest = balance * monthly_rate
    principal = payment - interest
    balance = balance - principal
    
    # Handle floating point precision for final payment
    if period == months:
        balance = 0.00
    
    print(f"{period},{payment:.2f},{principal:.2f},{interest:.2f},{balance:.2f}")