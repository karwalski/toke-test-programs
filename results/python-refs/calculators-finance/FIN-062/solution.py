income = float(input())

needs_total = 0
wants_total = 0
savings_total = 0

while True:
    try:
        line = input().strip()
        if not line:
            break
        parts = line.split()
        category = parts[0]
        amount = float(parts[1])
        
        if category == "needs":
            needs_total += amount
        elif category == "wants":
            wants_total += amount
        elif category == "savings":
            savings_total += amount
    except EOFError:
        break

needs_percent = (needs_total / income) * 100
wants_percent = (wants_total / income) * 100
savings_percent = (savings_total / income) * 100

print(f"needs: {needs_percent:.2f}% (target 50%)")
print(f"wants: {wants_percent:.2f}% (target 30%)")
print(f"savings: {savings_percent:.2f}% (target 20%)")