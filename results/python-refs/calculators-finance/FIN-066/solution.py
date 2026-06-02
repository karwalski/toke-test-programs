beginning_value, ending_value, years = input().split()
beginning_value = float(beginning_value)
ending_value = float(ending_value)
years = float(years)

cagr = ((ending_value / beginning_value) ** (1 / years) - 1) * 100
print(f"{cagr:.2f}%")