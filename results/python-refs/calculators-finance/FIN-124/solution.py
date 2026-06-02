import sys

# Read input
line = input().strip()
initial_deposit, monthly_deposit, annual_rate, years = line.split()

initial_deposit = float(initial_deposit)
monthly_deposit = float(monthly_deposit)
annual_rate = float(annual_rate)
years = int(years)

# Calculate compound interest with regular deposits
# Formula: compound interest is calculated monthly
monthly_rate = annual_rate / 12
total_months = years * 12

# Start with initial deposit
balance = initial_deposit

# For each month, add interest to current balance, then add monthly deposit
for month in range(total_months):
    # Add interest to current balance
    balance = balance * (1 + monthly_rate)
    # Add monthly deposit
    balance = balance + monthly_deposit

# Format to 2 decimal places
print(f"{balance:.2f}")