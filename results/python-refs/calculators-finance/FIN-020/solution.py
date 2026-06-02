nominal_rate, compounding_periods = input().split()
nominal_rate = float(nominal_rate)
compounding_periods = int(compounding_periods)

effective_rate = (1 + nominal_rate / compounding_periods) ** compounding_periods - 1
effective_rate_percentage = effective_rate * 100

print(f"{effective_rate_percentage:.4f}%")