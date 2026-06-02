future_value, rate, periods = input().split()
future_value = float(future_value)
rate = float(rate)
periods = int(periods)

present_value = future_value / ((1 + rate) ** periods)
print(f"{present_value:.2f}")