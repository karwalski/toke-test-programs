nominal_rate, inflation_rate = map(float, input().split())
real_rate = (1 + nominal_rate) / (1 + inflation_rate) - 1
print(f"{real_rate * 100:.4f}%")