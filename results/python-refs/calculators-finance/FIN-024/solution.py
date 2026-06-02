purchase_price, sale_price, holding_months, tax_rate = map(float, input().split())

capital_gain = sale_price - purchase_price

# Apply 50% discount if held over 12 months
if holding_months > 12:
    discounted_gain = capital_gain * 0.5
else:
    discounted_gain = capital_gain

tax_payable = discounted_gain * tax_rate

print(f"{discounted_gain:.2f}")
print(f"{tax_payable:.2f}")