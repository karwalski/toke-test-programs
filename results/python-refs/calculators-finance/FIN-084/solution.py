present_value, rate, periods = input().split()
present_value = float(present_value)
rate = float(rate)
periods = int(periods)

future_value = present_value * (1 + rate) ** periods
print(f"{future_value:.2f}")