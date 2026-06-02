import sys
import csv
import json

def calculate_trend(batches, yields):
    if len(batches) < 2:
        return 0, "stable", False
    
    n = len(batches)
    sum_x = sum(batches)
    sum_y = sum(yields)
    sum_xy = sum(x * y for x, y in zip(batches, yields))
    sum_x_sq = sum(x * x for x in batches)
    
    # Calculate slope using least squares regression
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_sq - sum_x * sum_x)
    
    # Determine trend direction
    if slope > 0.1:
        trend_direction = "increasing"
    elif slope < -0.1:
        trend_direction = "decreasing"
    else:
        trend_direction = "stable"
    
    # Alert if decreasing trend or slope magnitude > 0.5
    alert = trend_direction == "decreasing" or abs(slope) > 0.5
    
    return slope, trend_direction, alert

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
batches = []
yields = []

for row in reader:
    batches.append(int(row['batch_number']))
    yields.append(float(row['yield_percent']))

slope, trend_direction, alert = calculate_trend(batches, yields)

result = {
    "trend_direction": trend_direction,
    "slope": slope,
    "alert": alert
}

print(json.dumps(result, separators=(',', ':')))