import json
import sys
import statistics

def detect_anomaly(data):
    history = data['history']
    current = data['current']
    threshold_multiplier = data['threshold_multiplier']
    
    # Extract historical costs
    historical_costs = [entry['cost'] for entry in history]
    current_cost = current['cost']
    
    # Calculate mean and standard deviation
    mean_cost = statistics.mean(historical_costs)
    stdev_cost = statistics.stdev(historical_costs) if len(historical_costs) > 1 else 0
    
    # Calculate expected range
    min_expected = max(0, mean_cost - threshold_multiplier * stdev_cost)
    max_expected = mean_cost + threshold_multiplier * stdev_cost
    
    # Check if current cost is anomalous
    is_anomaly = current_cost < min_expected or current_cost > max_expected
    
    # Calculate deviation percentage
    if current_cost > max_expected:
        deviation_pct = ((current_cost - mean_cost) / mean_cost) * 100
    elif current_cost < min_expected:
        deviation_pct = ((mean_cost - current_cost) / mean_cost) * 100
    else:
        deviation_pct = 0.0
    
    # Round to handle floating point precision
    deviation_pct = round(deviation_pct, 1)
    min_expected = round(min_expected, 1)
    max_expected = round(max_expected, 1)
    
    result = {
        "is_anomaly": is_anomaly,
        "expected_range": {
            "min": min_expected,
            "max": max_expected
        },
        "deviation_pct": deviation_pct
    }
    
    return result

# Read input from stdin
input_data = json.loads(sys.stdin.read())

# Process the data
result = detect_anomaly(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))