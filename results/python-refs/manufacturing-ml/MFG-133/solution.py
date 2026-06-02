import sys
import csv
import json
import math

def main():
    lines = [line.rstrip('\n') for line in sys.stdin if line.strip()]
    reader = csv.reader(lines)
    rows = list(reader)
    
    target_types = rows[0][1:]
    target_values = [float(x) for x in rows[1][1:]]
    headers = rows[2]
    response_cols = headers[1:]
    
    data_rows = []
    for i in range(3, len(rows)):
        row = rows[i]
        x_val = float(row[0])
        responses = [float(x) for x in row[1:]]
        data_rows.append((x_val, responses))
    
    num_responses = len(response_cols)
    min_vals = [float('inf')] * num_responses
    max_vals = [float('-inf')] * num_responses
    
    for x_val, responses in data_rows:
        for j, resp in enumerate(responses):
            min_vals[j] = min(min_vals[j], resp)
            max_vals[j] = max(max_vals[j], resp)
    
    # For Derringer-Suich:
    # maximize: target is upper goal T, min observed is L
    #   d = (y - L) / (T - L), clipped, but if y >= T then 1
    # minimize: target is lower goal T, max observed is U
    #   d = (U - y) / (U - T), clipped, if y <= T then 1
    
    def desirability(value, target_type, target_value, lo, hi):
        if target_type == "maximize":
            T = target_value
            L = lo
            if value >= T:
                return 1.0
            if value <= L:
                return 0.0
            return (value - L) / (T - L)
        elif target_type == "minimize":
            T = target_value
            U = hi
            if value <= T:
                return 1.0
            if value >= U:
                return 0.0
            return (U - value) / (U - T)
        return 0.0
    
    overall_desirabilities = []
    for x_val, responses in data_rows:
        ds = []
        for j, resp in enumerate(responses):
            d = desirability(resp, target_types[j], target_values[j], min_vals[j], max_vals[j])
            ds.append(d)
        prod = 1.0
        for d in ds:
            prod *= d
        if prod <= 0:
            overall = 0.0
        else:
            overall = prod ** (1.0/len(ds))
        overall_desirabilities.append(overall)
    
    max_des = max(overall_desirabilities)
    optimal_idx = overall_desirabilities.index(max_des)
    optimal_x = int(data_rows[optimal_idx][0])
    
    rounded = [round(d, 2) for d in overall_desirabilities]
    
    result = {
        "desirabilities": rounded,
        "optimal_x": optimal_x,
        "overall_desirability": round(max_des, 2)
    }
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()