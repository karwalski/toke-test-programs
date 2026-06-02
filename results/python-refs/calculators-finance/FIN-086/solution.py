payment, rate, periods = input().split()
payment = float(payment)
rate = float(rate)
periods = int(periods)

future_value = payment * (((1 + rate) ** periods - 1) / rate)

print(f"{future_value:.2f}")