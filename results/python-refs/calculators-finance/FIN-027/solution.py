import sys

# Read weekly gross income
weekly_gross = float(input().strip())

# Read tax brackets
brackets = []
for line in sys.stdin:
    line = line.strip()
    if line:
        threshold, rate = line.split()
        brackets.append((float(threshold), float(rate)))

# Calculate PAYG tax withholding
tax = 0.0
previous_threshold = 0.0

for threshold, rate in brackets:
    if weekly_gross <= threshold:
        # Apply current rate to remaining income
        taxable_amount = weekly_gross - previous_threshold
        tax += taxable_amount * rate
        break
    else:
        # Apply current rate to this bracket's range
        taxable_amount = threshold - previous_threshold
        tax += taxable_amount * rate
        previous_threshold = threshold

# If income exceeds all thresholds, apply highest rate to remaining amount
if weekly_gross > brackets[-1][0]:
    remaining_income = weekly_gross - brackets[-1][0]
    tax += remaining_income * brackets[-1][1]

# Output result to 2 decimal places
print(f"{tax:.2f}")