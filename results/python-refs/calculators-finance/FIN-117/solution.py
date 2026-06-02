import sys
import math

def calculate_loan_metrics(principal, annual_rate, years):
    # Convert annual rate to monthly rate
    monthly_rate = annual_rate / 12
    # Convert years to months
    num_payments = years * 12
    
    # Calculate monthly payment using the formula:
    # M = P * [r(1+r)^n] / [(1+r)^n - 1]
    if monthly_rate == 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    
    # Calculate total amount paid
    total_paid = monthly_payment * num_payments
    
    # Calculate total interest
    total_interest = total_paid - principal
    
    return monthly_payment, total_interest, total_paid

# Read input and process each loan
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    name = parts[0]
    amount = float(parts[1])
    rate = float(parts[2])
    years = int(parts[3])
    
    monthly_payment, total_interest, total_cost = calculate_loan_metrics(amount, rate, years)
    
    print(f"{name} {monthly_payment:.2f} {total_interest:.2f} {total_cost:.2f}")