import sys

line = input().strip()
parts = line.split()
base_rate = float(parts[0])
age = int(parts[1])
risk_factors = [float(x) for x in parts[2].split(',')]

# Calculate age factor
if age < 25:
    age_factor = 1.5
elif age < 40:
    age_factor = 1.0
elif age < 65:
    age_factor = 0.8
else:
    age_factor = 1.2

# Calculate premium
premium = base_rate * age_factor
for risk_factor in risk_factors:
    premium *= risk_factor

print(f"{premium:.2f}")