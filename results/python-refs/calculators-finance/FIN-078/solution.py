property_value, annual_rent, annual_expenses, purchase_costs = map(int, input().split())

gross_yield = (annual_rent / property_value) * 100
net_yield = ((annual_rent - annual_expenses) / (property_value + purchase_costs)) * 100

print(f"{gross_yield:.2f}%")
print(f"{net_yield:.2f}%")