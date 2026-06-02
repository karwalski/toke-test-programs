import sys

# Read input
line1 = input().strip()
alpha, forecast_periods = line1.split()
alpha = float(alpha)
forecast_periods = int(forecast_periods)

line2 = input().strip()
historical_values = [float(x) for x in line2.split(',')]

# Apply single exponential smoothing
# Initialize with first value
smoothed = historical_values[0]

# Calculate smoothed values for the rest of the series
for i in range(1, len(historical_values)):
    smoothed = alpha * historical_values[i] + (1 - alpha) * smoothed

# The forecast for all future periods is the last smoothed value
forecast_values = [smoothed] * forecast_periods

# Format output to 2 decimal places
output = ','.join(f"{value:.2f}" for value in forecast_values)
print(output)