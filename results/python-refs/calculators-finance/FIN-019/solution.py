import math

rate = float(input())
rule_of_72 = 72 / rate
exact_years = math.log(2) / math.log(1 + rate / 100)

print(f"{rule_of_72:.2f}")
print(f"{exact_years:.2f}")