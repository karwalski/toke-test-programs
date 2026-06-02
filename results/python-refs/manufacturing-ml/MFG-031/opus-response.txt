import sys
import json

lines = sys.stdin.read().strip().split('\n')
alpha, beta = map(float, lines[0].split(','))
values = list(map(float, lines[1].split(',')))

# Try initialization: level=values[0], trend=values[1]-values[0]
# Start loop from i=1
level = values[0]
trend = values[1] - values[0]

for i in range(2, len(values)):
    prev_level = level
    level = alpha * values[i] + (1 - alpha) * (level + trend)
    trend = beta * (level - prev_level) + (1 - beta) * trend

forecast_next = level + trend

result = {
    "forecast_next": round(forecast_next, 2),
    "level": round(level, 2),
    "trend": round(trend, 2)
}

print(json.dumps(result, separators=(',', ':')))