goal, current_savings, months, annual_rate = input().split()
goal = float(goal)
current_savings = float(current_savings)
months = int(months)
annual_rate = float(annual_rate)

monthly_rate = annual_rate / 12
amount_needed = goal - current_savings

if annual_rate == 0:
    monthly_deposit = amount_needed / months
else:
    # Future value of current savings with compound interest
    future_value_current = current_savings * ((1 + monthly_rate) ** months)
    
    # Amount still needed after current savings grow
    remaining_needed = goal - future_value_current
    
    # Calculate monthly deposit using annuity formula
    # PMT = FV / (((1 + r)^n - 1) / r)
    if remaining_needed <= 0:
        monthly_deposit = 0
    else:
        monthly_deposit = remaining_needed / (((1 + monthly_rate) ** months - 1) / monthly_rate)

print(f"{monthly_deposit:.2f}")