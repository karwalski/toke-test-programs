fixed_costs, variable_cost_per_unit, selling_price_per_unit = map(float, input().split())

break_even_units = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
break_even_revenue = break_even_units * selling_price_per_unit

print(int(break_even_units))
print(f"{break_even_revenue:.2f}")