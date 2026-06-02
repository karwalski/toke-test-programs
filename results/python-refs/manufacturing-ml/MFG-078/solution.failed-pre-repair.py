import sys
import csv
import json
import math

def calculate_true_position(nominal_x, nominal_y, actual_x, actual_y):
    """Calculate true position using the formula: sqrt((actual_x - nominal_x)^2 + (actual_y - nominal_y)^2)"""
    delta_x = actual_x - nominal_x
    delta_y = actual_y - nominal_y
    true_position = math.sqrt(delta_x**2 + delta_y**2)
    return true_position

def main():
    # Read CSV from stdin
    csv_reader = csv.DictReader(sys.stdin)
    
    features = []
    
    for row in csv_reader:
        nominal_x = float(row['nominal_x'])
        nominal_y = float(row['nominal_y'])
        actual_x = float(row['actual_x'])
        actual_y = float(row['actual_y'])
        tolerance = float(row['tolerance'])
        
        true_position = calculate_true_position(nominal_x, nominal_y, actual_x, actual_y)
        
        # Round to 2 decimal places to match expected output
        true_position = round(true_position, 2)
        
        # Check if it passes (true position <= tolerance)
        pass_check = true_position <= tolerance
        
        features.append({
            "true_position": true_position,
            "tolerance": tolerance,
            "pass": pass_check
        })
    
    # Output JSON
    result = {"features": features}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()