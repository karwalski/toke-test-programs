principal, rate, years = input().split()
principal = float(principal)
rate = float(rate)
years = float(years)

interest = principal * rate * years
total = principal + interest

print(f"{interest:.2f}")
print(f"{total:.2f}")