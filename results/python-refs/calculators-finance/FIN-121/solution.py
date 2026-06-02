import sys
import math

def calculate_months_to_payoff(balance, rate, payment):
    if payment <= 0:
        return float('inf')
    
    monthly_rate = rate / 12
    if monthly_rate == 0:
        return math.ceil(balance / payment)
    
    if payment <= balance * monthly_rate:
        return float('inf')
    
    months = math.log(1 + (balance * monthly_rate) / (payment - balance * monthly_rate)) / math.log(1 + monthly_rate)
    return math.ceil(months)

def debt_snowball(extra_payment, debts):
    # Sort debts by balance (smallest first)
    debts.sort(key=lambda x: x[1])
    
    results = []
    cumulative_months = 0
    total_extra = extra_payment
    
    for i, (name, balance, rate, min_payment) in enumerate(debts):
        # Calculate payment for this debt (minimum + extra from previous paid-off debts + allocated extra)
        current_payment = min_payment + total_extra
        
        # Calculate months to pay off this debt
        months = calculate_months_to_payoff(balance, rate, current_payment)
        cumulative_months += months
        
        results.append((name, cumulative_months))
        
        # Add this debt's minimum payment to the extra amount for next debts
        total_extra += min_payment
    
    return results

# Read input
lines = sys.stdin.read().strip().split('\n')
extra_payment = int(lines[0])

debts = []
for line in lines[1:]:
    parts = line.split()
    name = parts[0]
    balance = float(parts[1])
    rate = float(parts[2])
    min_payment = float(parts[3])
    debts.append((name, balance, rate, min_payment))

# Calculate payoff order and timeline
results = debt_snowball(extra_payment, debts)

# Output results
for name, months in results:
    print(f"{name}: {int(months)} months")