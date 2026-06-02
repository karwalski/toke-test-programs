mode, amount, rate = input().split()
amount = float(amount)
rate = float(rate)

if mode == "exclusive":
    net_amount = amount
    tax_amount = amount * rate
else:  # inclusive
    net_amount = amount / (1 + rate)
    tax_amount = amount - net_amount

print(f"{net_amount:.2f}")
print(f"{tax_amount:.2f}")