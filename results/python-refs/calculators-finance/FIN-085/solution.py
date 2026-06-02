payment, rate, periods = input().split()
payment = float(payment)
rate = float(rate)
periods = int(periods)

present_value = payment * ((1 - (1 + rate) ** -periods) / rate)

print(f"{present_value:.2f}")