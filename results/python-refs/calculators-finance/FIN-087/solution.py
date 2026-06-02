payment, discount_rate, growth_rate = input().split()
payment = float(payment)
discount_rate = float(discount_rate)
growth_rate = float(growth_rate)

perpetuity_value = payment / discount_rate
growing_perpetuity_value = payment / (discount_rate - growth_rate)

print(f"{perpetuity_value:.2f}")
print(f"{growing_perpetuity_value:.2f}")