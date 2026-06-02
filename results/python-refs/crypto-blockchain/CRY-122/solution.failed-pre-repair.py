import json
import sys
import statistics

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON array of gas prices
gas_prices = json.loads(input_data)

# Sort the gas prices for percentile calculation
gas_prices.sort()

# Calculate percentiles
# For percentiles, we use the nearest-rank method
n = len(gas_prices)

# 25th percentile (slow)
p25_index = int(0.25 * (n - 1))
if 0.25 * (n - 1) == p25_index:
    p25 = gas_prices[p25_index]
else:
    # Linear interpolation
    lower_index = int(0.25 * (n - 1))
    upper_index = lower_index + 1
    weight = (0.25 * (n - 1)) - lower_index
    p25 = gas_prices[lower_index] * (1 - weight) + gas_prices[upper_index] * weight

# 50th percentile (average/median)
p50_index = int(0.5 * (n - 1))
if 0.5 * (n - 1) == p50_index:
    p50 = gas_prices[p50_index]
else:
    # Linear interpolation
    lower_index = int(0.5 * (n - 1))
    upper_index = lower_index + 1
    weight = (0.5 * (n - 1)) - lower_index
    p50 = gas_prices[lower_index] * (1 - weight) + gas_prices[upper_index] * weight

# 75th percentile (fast)
p75_index = int(0.75 * (n - 1))
if 0.75 * (n - 1) == p75_index:
    p75 = gas_prices[p75_index]
else:
    # Linear interpolation
    lower_index = int(0.75 * (n - 1))
    upper_index = lower_index + 1
    weight = (0.75 * (n - 1)) - lower_index
    p75 = gas_prices[lower_index] * (1 - weight) + gas_prices[upper_index] * weight

# Round to integers
slow = int(round(p25))
average = int(round(p50))
fast = int(round(p75))

# Output in the exact format required
print(f"slow:{slow} average:{average} fast:{fast}")