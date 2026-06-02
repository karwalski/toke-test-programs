import sys
import json

# Read input
lines = sys.stdin.read().strip().split('\n')
alpha, beta = map(float, lines[0].split(','))
values = list(map(int, lines[1].split(',')))

# Initialize first level and trend
level = values[0]
trend = values[1] - values[0] if len(values) > 1 else 0

# Apply Holt's double exponential smoothing
for i in range(1, len(values)):
    prev_level = level
    level = alpha * values[i] + (1 - alpha) * (level + trend)
    trend = beta * (level - prev_level) + (1 - beta) * trend

# Forecast next value
forecast_next = level + trend

# Output as JSON
result = {
    "forecast_next": round(forecast_next, 2),
    "level": round(level, 2),
    "trend": round(trend, 2)
}

print(json.dumps(result, separators=(',', ':')))