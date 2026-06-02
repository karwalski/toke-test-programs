import sys
import json
import statistics

def detect_spc_violations(measurements):
    violations = []
    n = len(measurements)
    
    if n < 7:
        return violations
    
    # Calculate mean and standard deviation for control limits
    mean = statistics.mean(measurements)
    stdev = statistics.stdev(measurements) if n > 1 else 0
    
    # Rule 1: 7 points trending up or down
    for i in range(n - 6):
        # Check for 7 consecutive increasing points
        increasing = True
        decreasing = True
        
        for j in range(i, i + 6):
            if measurements[j + 1] <= measurements[j]:
                increasing = False
            if measurements[j + 1] >= measurements[j]:
                decreasing = False
        
        if increasing or decreasing:
            violations.append({
                "rule": "7_points_trending",
                "start_index": i
            })
    
    # Rule 2: 7 points on one side of mean
    if stdev > 0:
        for i in range(n - 6):
            above_mean = all(measurements[j] > mean for j in range(i, i + 7))
            below_mean = all(measurements[j] < mean for j in range(i, i + 7))
            
            if above_mean or below_mean:
                violations.append({
                    "rule": "7_points_one_side",
                    "start_index": i
                })
    
    # Rule 3: 14 points alternating up and down (oscillation)
    if n >= 14:
        for i in range(n - 13):
            alternating = True
            for j in range(i, i + 12):
                if j % 2 == 0:  # Even positions should go up
                    if measurements[j + 1] <= measurements[j]:
                        alternating = False
                        break
                else:  # Odd positions should go down
                    if measurements[j + 1] >= measurements[j]:
                        alternating = False
                        break
            
            if alternating:
                violations.append({
                    "rule": "14_points_oscillating",
                    "start_index": i
                })
    
    # Rule 4: 15 points close to center line (hugging)
    if stdev > 0 and n >= 15:
        for i in range(n - 14):
            hugging = all(abs(measurements[j] - mean) < stdev for j in range(i, i + 15))
            
            if hugging:
                violations.append({
                    "rule": "15_points_hugging",
                    "start_index": i
                })
    
    return violations

# Read input from stdin
input_line = sys.stdin.read().strip()
measurements = [float(x) for x in input_line.split(',')]

# Detect violations
violations = detect_spc_violations(measurements)

# Output JSON
result = {"rule_violations": violations}
print(json.dumps(result, separators=(',', ':')))