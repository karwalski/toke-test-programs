alpha = float(input().strip())
values = list(map(float, input().strip().split(',')))

ema_values = []
ema = values[0]  # First EMA value is the first data point
ema_values.append(ema)

for i in range(1, len(values)):
    ema = alpha * values[i] + (1 - alpha) * ema
    ema_values.append(ema)

# Format to 2 decimal places and join with commas
output = ','.join(f"{val:.2f}" for val in ema_values)
print(output)