import json
import sys

# Read input
config_line = input().strip()
stats_line = input().strip()

config = json.loads(config_line)
stats = json.loads(stats_line)

# Extract values
max_depth = config["max_depth"]
warn_threshold = config["warn_threshold"]
critical_threshold = config["critical_threshold"]

depth = stats["depth"]
rate_in = stats["rate_in"]
rate_out = stats["rate_out"]
consumer_lag_ms = stats["consumer_lag_ms"]

# Calculate percentage full
pct_full = depth / max_depth

# Determine backpressure signal
if pct_full >= critical_threshold:
    if pct_full >= 1.0:
        signal = "FULL"
    else:
        signal = "CRITICAL"
elif pct_full >= warn_threshold:
    signal = "WARN"
else:
    signal = "NONE"

# Calculate deficit
deficit = rate_in - rate_out

# Calculate time to full
if deficit > 0:
    remaining_capacity = max_depth - depth
    time_to_full = remaining_capacity / deficit
else:
    time_to_full = float('inf')

# Calculate recommended action
if deficit > 0:
    reduction_pct = (deficit / rate_in) * 100
    action = f"reduce producer rate by {reduction_pct:.0f}%"
else:
    action = "no action needed"

# Format output
pct_display = int(pct_full * 100)
print(f"{signal} ({pct_display}% full)")
print(f"rate: in={rate_in}/s, out={rate_out}/s (deficit: {deficit}/s)")
print(f"lag: {consumer_lag_ms}ms")
if time_to_full != float('inf'):
    print(f"time to full: {time_to_full}s")
else:
    print("time to full: never")
print(f"action: {action}")