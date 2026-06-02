loan_amount, rate, periods, balloon_amount = input().split()
loan_amount = float(loan_amount)
rate = float(rate)
periods = int(periods)
balloon_amount = float(balloon_amount)

# Calculate the periodic payment with balloon payment
# Formula: PMT = (PV - BV * (1 + r)^(-n)) * r / (1 - (1 + r)^(-n))
# Where PV = loan amount, BV = balloon amount, r = rate, n = periods

discount_factor = (1 + rate) ** (-periods)
present_value_of_balloon = balloon_amount * discount_factor
annuity_factor = (1 - discount_factor) / rate

periodic_payment = (loan_amount - present_value_of_balloon) / annuity_factor

print(f"{periodic_payment:.2f}")