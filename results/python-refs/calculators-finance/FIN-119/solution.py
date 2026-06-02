import sys

# Read input
line = input().strip()
principal, annual_rate, months = line.split()
principal = float(principal)
annual_rate = float(annual_rate)
months = int(months)

# Calculate monthly interest rate
monthly_rate = annual_rate / 12

# Calculate EMI using the formula
if monthly_rate == 0:
    emi = principal / months
else:
    emi = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)

# Calculate total payment and total interest
total_payment = emi * months
total_interest = total_payment - principal

# Output results
print(f"{emi:.2f}")
print(f"{total_payment:.2f}")
print(f"{total_interest:.2f}")