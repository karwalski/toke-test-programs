import sys

assets_total = 0.0
liabilities_total = 0.0
equity_total = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    entry_type = parts[0]
    account = parts[1]
    amount = float(parts[2])
    
    if entry_type == "ASSET":
        assets_total += amount
    elif entry_type == "LIABILITY":
        liabilities_total += amount
    elif entry_type == "EQUITY":
        equity_total += amount

print(f"ASSETS: {assets_total:.2f}")
print(f"LIABILITIES: {liabilities_total:.2f}")
print(f"EQUITY: {equity_total:.2f}")

if abs(assets_total - (liabilities_total + equity_total)) < 0.01:
    print("BALANCED")
else:
    print("NOT BALANCED")