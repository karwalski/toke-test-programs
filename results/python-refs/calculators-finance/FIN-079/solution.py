net_operating_income, property_value = map(float, input().split())
cap_rate = (net_operating_income / property_value) * 100
print(f"{cap_rate:.2f}%")