import sys

# Read all input lines
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse input
items = []
tax_rate = 0.0

for line in lines:
    if line.startswith('TAX'):
        parts = line.split()
        tax_rate = float(parts[1])
    else:
        parts = line.split()
        item_name = parts[0]
        qty = int(parts[1])
        unit_price = float(parts[2])
        discount_pct = float(parts[3])
        items.append((item_name, qty, unit_price, discount_pct))

# Calculate totals
subtotal = 0.0
total_discount = 0.0

for item_name, qty, unit_price, discount_pct in items:
    line_total = qty * unit_price
    line_discount = line_total * (discount_pct / 100.0)
    subtotal += line_total
    total_discount += line_discount

# Calculate after discount and tax
after_discount = subtotal - total_discount
tax_amount = after_discount * tax_rate
grand_total = after_discount + tax_amount

# Output
print(f"{subtotal:.2f}")
print(f"{total_discount:.2f}")
print(f"{tax_amount:.2f}")
print(f"{grand_total:.2f}")