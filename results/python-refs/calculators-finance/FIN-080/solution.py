import sys
import math

def calculate_mortgage(principal, annual_rate, years):
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    
    total_cost = monthly_payment * num_payments
    return monthly_payment, total_cost

# Read input
line1 = input().strip().split()
line2 = input().strip().split()

# Parse option 1
amount1 = float(line1[0])
rate1 = float(line1[1])
years1 = int(line1[2])

# Parse option 2
amount2 = float(line2[0])
rate2 = float(line2[1])
years2 = int(line2[2])

# Calculate mortgage payments
monthly1, total1 = calculate_mortgage(amount1, rate1, years1)
monthly2, total2 = calculate_mortgage(amount2, rate2, years2)

# Print results
print(f"Option1: {monthly1:.2f}/month, {total1:.2f} total")
print(f"Option2: {monthly2:.2f}/month, {total2:.2f} total")

# Recommend cheaper option
if total1 < total2:
    print("RECOMMEND: Option1")
else:
    print("RECOMMEND: Option2")