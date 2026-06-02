import csv
import sys
import json

# Read CSV data from stdin
reader = csv.DictReader(sys.stdin)
data = list(reader)

# Extract data
cycles = [int(row['cycle']) for row in data]
wear_measurements = [float(row['wear_measurement']) for row in data]
max_wear = float(data[0]['max_wear'])

# Calculate wear rate using linear regression
n = len(cycles)
sum_x = sum(cycles)
sum_y = sum(wear_measurements)
sum_xy = sum(x * y for x, y in zip(cycles, wear_measurements))
sum_x2 = sum(x * x for x in cycles)

# Calculate slope (wear rate)
wear_rate = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)

# Calculate intercept
intercept = (sum_y - wear_rate * sum_x) / n

# Calculate replacement cycle (when wear reaches max_wear)
replacement_cycle = int((max_wear - intercept) / wear_rate)

# Calculate cycles remaining from last data point
last_cycle = cycles[-1]
cycles_remaining = replacement_cycle - last_cycle

# Output JSON
result = {
    "wear_rate": wear_rate,
    "cycles_remaining": cycles_remaining,
    "replacement_cycle": replacement_cycle
}

print(json.dumps(result, separators=(',', ':')))