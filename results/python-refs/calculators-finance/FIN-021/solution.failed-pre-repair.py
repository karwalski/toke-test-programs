income = float(input())
brackets = []

try:
    while True:
        line = input().strip()
        if line:
            threshold, rate = line.split()
            brackets.append((float(threshold), float(rate)))
except EOFError:
    pass

# Sort brackets by threshold
brackets.sort()

total_tax = 0.0
prev_threshold = 0.0

for threshold, rate in brackets:
    if income > threshold:
        # Tax the portion from prev_threshold to threshold at the previous rate
        if len([b for b in brackets if b[0] <= prev_threshold]) > 0:
            prev_rate = [b[1] for b in brackets if b[0] <= prev_threshold][-1]
        else:
            prev_rate = 0.0
        
        taxable_amount = min(income, threshold) - prev_threshold
        if prev_threshold > 0 or threshold > prev_threshold:
            total_tax += taxable_amount * prev_rate
        prev_threshold = threshold
    else:
        break

# Tax remaining income at the current rate
if income > prev_threshold:
    remaining_income = income - prev_threshold
    current_rate = [b[1] for b in brackets if b[0] <= prev_threshold][-1] if prev_threshold > 0 else 0.0
    total_tax += remaining_income * current_rate

print(f"{total_tax:.2f}")