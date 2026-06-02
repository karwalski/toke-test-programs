import sys

# Read input
line = input().strip()
current_age, retire_age, monthly_expense, inflation_rate, return_rate = line.split()

current_age = int(current_age)
retire_age = int(retire_age)
monthly_expense = float(monthly_expense)
inflation_rate = float(inflation_rate)
return_rate = float(return_rate)

# Calculate years to retirement
years_to_retirement = retire_age - current_age

# Calculate future monthly expense at retirement (adjusted for inflation)
future_monthly_expense = monthly_expense * ((1 + inflation_rate) ** years_to_retirement)

# Calculate annual expense at retirement
annual_expense = future_monthly_expense * 12

# Assume retirement period of 25 years (common assumption)
# Calculate corpus needed using present value of annuity formula
# Assuming expenses grow at inflation rate during retirement too
retirement_years = 25
real_return_rate = (1 + return_rate) / (1 + inflation_rate) - 1

if real_return_rate > 0:
    # Present value of growing annuity
    corpus_needed = annual_expense * ((1 - ((1 + inflation_rate) / (1 + return_rate)) ** retirement_years) / (return_rate - inflation_rate))
else:
    corpus_needed = annual_expense * retirement_years

# Calculate monthly savings required using future value of annuity formula
monthly_return_rate = return_rate / 12
months_to_retirement = years_to_retirement * 12

if monthly_return_rate > 0:
    monthly_savings = corpus_needed * monthly_return_rate / (((1 + monthly_return_rate) ** months_to_retirement) - 1)
else:
    monthly_savings = corpus_needed / months_to_retirement

# Calculate total invested
total_invested = monthly_savings * months_to_retirement

# Output results
print(f"{corpus_needed:.2f}")
print(f"{monthly_savings:.2f}")
print(f"{total_invested:.2f}")