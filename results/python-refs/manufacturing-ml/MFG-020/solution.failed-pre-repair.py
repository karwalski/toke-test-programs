import sys
import json
import math

def calculate_stats(data):
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)
    return mean, std_dev

def detect_nelson_violations(data):
    violations = []
    n = len(data)
    
    if n < 2:
        return violations
    
    mean, sigma = calculate_stats(data)
    
    for i in range(n):
        value = data[i]
        
        # Rule 1: Point beyond 3 sigma
        if abs(value - mean) > 3 * sigma:
            violations.append({
                "rule": 1,
                "index": i,
                "description": "point beyond 3 sigma"
            })
        
        # Rule 2: 9 consecutive points on same side of mean
        if i >= 8:
            same_side = True
            first_side = data[i-8] > mean
            for j in range(i-8, i+1):
                if (data[j] > mean) != first_side:
                    same_side = False
                    break
            if same_side:
                violations.append({
                    "rule": 2,
                    "index": i,
                    "description": "9 consecutive points on same side of mean"
                })
        
        # Rule 3: 6 consecutive increasing or decreasing points
        if i >= 5:
            increasing = True
            decreasing = True
            for j in range(i-4, i+1):
                if data[j] <= data[j-1]:
                    increasing = False
                if data[j] >= data[j-1]:
                    decreasing = False
            if increasing or decreasing:
                violations.append({
                    "rule": 3,
                    "index": i,
                    "description": "6 consecutive increasing or decreasing points"
                })
        
        # Rule 4: 14 consecutive alternating points
        if i >= 13:
            alternating = True
            for j in range(i-12, i+1):
                if j == i-12:
                    continue
                prev_direction = data[j-1] > data[j-2] if j > i-12 else None
                curr_direction = data[j] > data[j-1]
                if prev_direction is not None and prev_direction == curr_direction:
                    alternating = False
                    break
            if alternating:
                violations.append({
                    "rule": 4,
                    "index": i,
                    "description": "14 consecutive alternating points"
                })
        
        # Rule 5: 2 out of 3 consecutive points beyond 2 sigma
        if i >= 2:
            beyond_2sigma_count = 0
            for j in range(i-2, i+1):
                if abs(data[j] - mean) > 2 * sigma:
                    beyond_2sigma_count += 1
            if beyond_2sigma_count >= 2:
                violations.append({
                    "rule": 5,
                    "index": i,
                    "description": "2 out of 3 consecutive points beyond 2 sigma"
                })
        
        # Rule 6: 4 out of 5 consecutive points beyond 1 sigma
        if i >= 4:
            beyond_1sigma_count = 0
            for j in range(i-4, i+1):
                if abs(data[j] - mean) > 1 * sigma:
                    beyond_1sigma_count += 1
            if beyond_1sigma_count >= 4:
                violations.append({
                    "rule": 6,
                    "index": i,
                    "description": "4 out of 5 consecutive points beyond 1 sigma"
                })
        
        # Rule 7: 15 consecutive points within 1 sigma
        if i >= 14:
            all_within_1sigma = True
            for j in range(i-14, i+1):
                if abs(data[j] - mean) > 1 * sigma:
                    all_within_1sigma = False
                    break
            if all_within_1sigma:
                violations.append({
                    "rule": 7,
                    "index": i,
                    "description": "15 consecutive points within 1 sigma"
                })
        
        # Rule 8: 8 consecutive points beyond 1 sigma on both sides
        if i >= 7:
            all_beyond_1sigma = True
            for j in range(i-7, i+1):
                if abs(data[j] - mean) <= 1 * sigma:
                    all_beyond_1sigma = False
                    break
            if all_beyond_1sigma:
                violations.append({
                    "rule": 8,
                    "index": i,
                    "description": "8 consecutive points beyond 1 sigma on both sides"
                })
    
    return violations

# Read input from stdin
input_line = sys.stdin.read().strip()
data = [float(x) for x in input_line.split(',')]

# Detect violations
violations = detect_nelson_violations(data)

# Output as JSON
result = {"violations": violations}
print(json.dumps(result, separators=(',', ':')))