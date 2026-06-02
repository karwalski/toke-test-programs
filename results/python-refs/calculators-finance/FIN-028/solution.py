import sys

total_before_tax = 0.0
total_tax = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    item_name = parts[0]
    quantity = int(parts[1])
    unit_price = float(parts[2])
    tax_rate = float(parts[3])
    
    item_total = quantity * unit_price
    item_tax = item_total * tax_rate
    
    total_before_tax += item_total
    total_tax += item_tax

grand_total = total_before_tax + total_tax

print(f"{total_before_tax:.2f}")
print(f"{total_tax:.2f}")
print(f"{grand_total:.2f}")