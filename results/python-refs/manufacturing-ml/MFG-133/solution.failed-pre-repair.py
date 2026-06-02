import sys
import csv
import json
import math

def calculate_desirability(value, target_type, target_value, min_val, max_val):
    if target_type == "maximize":
        if target_value <= min_val:
            return 1.0 if value >= target_value else 0.0
        desirability = (value - min_val) / (target_value - min_val)
        return min(1.0, max(0.0, desirability))
    elif target_type == "minimize":
        if target_value >= max_val:
            return 1.0 if value <= target_value else 0.0
        desirability = (max_val - value) / (max_val - target_value)
        return min(1.0, max(0.0, desirability))
    return 0.0

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse input
    reader = csv.reader(lines)
    rows = list(reader)
    
    # Parse target types
    target_types = rows[0][1:]
    
    # Parse target values
    target_values = [float(x) for x in rows[1][1:]]
    
    # Parse data
    headers = rows[2]
    x_col = headers[0]
    response_cols = headers[1:]
    
    data_rows = []
    for i in range(3, len(rows)):
        row = rows[i]
        x_val = float(row[0])
        responses = [float(x) for x in row[1:]]
        data_rows.append((x_val, responses))
    
    # Calculate min/max for each response
    num_responses = len(response_cols)
    min_vals = [float('inf')] * num_responses
    max_vals = [float('-inf')] * num_responses
    
    for x_val, responses in data_rows:
        for j, resp in enumerate(responses):
            min_vals[j] = min(min_vals[j], resp)
            max_vals[j] = max(max_vals[j], resp)
    
    # Calculate desirabilities
    overall_desirabilities = []
    
    for x_val, responses in data_rows:
        individual_desirabilities = []
        
        for j, resp in enumerate(responses):
            des = calculate_desirability(
                resp, 
                target_types[j], 
                target_values[j], 
                min_vals[j], 
                max_vals[j]
            )
            individual_desirabilities.append(des)
        
        # Overall desirability is geometric mean
        if all(d > 0 for d in individual_desirabilities):
            overall_des = math.pow(math.prod(individual_desirabilities), 1.0/len(individual_desirabilities))
        else:
            overall_des = 0.0
            
        overall_desirabilities.append(overall_des)
    
    # Find optimal point
    max_des = max(overall_desirabilities)
    optimal_idx = overall_desirabilities.index(max_des)
    optimal_x = int(data_rows[optimal_idx][0])
    
    # Round desirabilities to 2 decimal places
    rounded_desirabilities = [round(d, 2) for d in overall_desirabilities]
    rounded_max_des = round(max_des, 2)
    
    # Output JSON
    result = {
        "desirabilities": rounded_desirabilities,
        "optimal_x": optimal_x,
        "overall_desirability": rounded_max_des
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()