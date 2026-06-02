import sys

revenue_total = 0.0
expense_total = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    if len(parts) >= 3:
        entry_type = parts[0]
        amount = float(parts[2])
        
        if entry_type == "REVENUE":
            revenue_total += amount
        elif entry_type == "EXPENSE":
            expense_total += amount

net_result = revenue_total - expense_total

print(f"REVENUE: {revenue_total:.2f}")
print(f"EXPENSES: {expense_total:.2f}")
if net_result >= 0:
    print(f"NET PROFIT: {net_result:.2f}")
else:
    print(f"NET LOSS: {abs(net_result):.2f}")