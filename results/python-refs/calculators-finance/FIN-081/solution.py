import sys

lines = sys.stdin.read().strip().split('\n')
property_price = int(lines[0])

brackets = []
for i in range(1, len(lines)):
    parts = lines[i].split()
    threshold = int(parts[0])
    rate = float(parts[1])
    brackets.append((threshold, rate))

# Sort brackets by threshold
brackets.sort()

total_duty = 0.0
previous_threshold = 0

for threshold, rate in brackets:
    if property_price <= previous_threshold:
        break
    
    # Calculate the amount in this bracket
    amount_in_bracket = min(property_price, threshold) - previous_threshold
    
    if amount_in_bracket > 0:
        duty_for_bracket = amount_in_bracket * rate
        total_duty += duty_for_bracket
    
    previous_threshold = threshold

# If property price exceeds the highest threshold, apply the highest rate to the remainder
if property_price > brackets[-1][0]:
    remaining_amount = property_price - brackets[-1][0]
    total_duty += remaining_amount * brackets[-1][1]

print(f"{total_duty:.2f}")