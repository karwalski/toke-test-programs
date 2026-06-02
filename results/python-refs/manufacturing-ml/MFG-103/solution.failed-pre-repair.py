import sys
import csv
import json
from io import StringIO

def main():
    # Read CSV data from stdin
    input_data = sys.stdin.read().strip()
    
    # Parse CSV
    csv_reader = csv.DictReader(StringIO(input_data))
    data = list(csv_reader)
    
    # Extract data and convert to appropriate types
    months = []
    failures = []
    units_in_field = []
    costs_per_failure = []
    
    for row in data:
        months.append(int(row['month']))
        failures.append(int(row['failures']))
        units_in_field.append(int(row['units_in_field']))
        costs_per_failure.append(float(row['cost_per_failure']))
    
    # Calculate failure rates for each month
    failure_rates = []
    for i in range(len(data)):
        rate = failures[i] / units_in_field[i]
        failure_rates.append(rate)
    
    # Calculate average failure rate
    avg_failure_rate = sum(failure_rates) / len(failure_rates)
    
    # Determine trend
    if len(failure_rates) > 1:
        if failure_rates[-1] > failure_rates[0]:
            trend = "increasing"
        elif failure_rates[-1] < failure_rates[0]:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "stable"
    
    # Predict next month's cost
    # Use the trend to estimate next month's failure rate
    if trend == "increasing":
        # Calculate the rate of increase
        rate_diff = failure_rates[-1] - failure_rates[0]
        steps = len(failure_rates) - 1
        rate_increase_per_month = rate_diff / steps if steps > 0 else 0
        next_failure_rate = failure_rates[-1] + rate_increase_per_month
    elif trend == "decreasing":
        # Calculate the rate of decrease
        rate_diff = failure_rates[0] - failure_rates[-1]
        steps = len(failure_rates) - 1
        rate_decrease_per_month = rate_diff / steps if steps > 0 else 0
        next_failure_rate = failure_rates[-1] - rate_decrease_per_month
    else:
        next_failure_rate = avg_failure_rate
    
    # Estimate next month's units in field (assume growth continues)
    if len(units_in_field) > 1:
        unit_growth = units_in_field[-1] - units_in_field[-2]
        next_units = units_in_field[-1] + unit_growth
    else:
        next_units = units_in_field[-1]
    
    # Predict next month's failures and cost
    next_failures = next_failure_rate * next_units
    next_cost = next_failures * costs_per_failure[-1]
    
    # Round the results appropriately
    predicted_cost = int(round(next_cost))
    avg_failure_rate_rounded = round(avg_failure_rate, 5)
    
    # Create output JSON
    result = {
        "predicted_next_month_cost": predicted_cost,
        "failure_rate": avg_failure_rate_rounded,
        "trend": trend
    }
    
    # Output JSON
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()