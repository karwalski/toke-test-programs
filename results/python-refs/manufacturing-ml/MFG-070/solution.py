import sys
import json
import statistics

def detect_spc_violations(measurements):
    violations = []
    n = len(measurements)
    
    if n < 7:
        return violations
    
    mean = statistics.mean(measurements)
    stdev = statistics.stdev(measurements) if n > 1 else 0
    
    # Rule 1: 7 points trending - report only non-overlapping
    i = 0
    while i <= n - 7:
        increasing = all(measurements[j + 1] > measurements[j] for j in range(i, i + 6))
        decreasing = all(measurements[j + 1] < measurements[j] for j in range(i, i + 6))
        
        if increasing or decreasing:
            violations.append({
                "rule": "7_points_trending",
                "start_index": i
            })
            # Extend the run as far as it continues, then skip past it
            k = i + 6
            if increasing:
                while k + 1 < n and measurements[k + 1] > measurements[k]:
                    k += 1
            else:
                while k + 1 < n and measurements[k + 1] < measurements[k]:
                    k += 1
            i = k + 1
        else:
            i += 1
    
    # Rule 2: 7 points on one side of mean
    if stdev > 0:
        i = 0
        while i <= n - 7:
            above = all(measurements[j] > mean for j in range(i, i + 7))
            below = all(measurements[j] < mean for j in range(i, i + 7))
            if above or below:
                violations.append({
                    "rule": "7_points_one_side",
                    "start_index": i
                })
                k = i + 6
                if above:
                    while k + 1 < n and measurements[k + 1] > mean:
                        k += 1
                else:
                    while k + 1 < n and measurements[k + 1] < mean:
                        k += 1
                i = k + 1
            else:
                i += 1
    
    # Rule 3: 14 points alternating
    if n >= 14:
        i = 0
        while i <= n - 14:
            alternating = True
            for j in range(i, i + 13):
                if measurements[j + 1] == measurements[j]:
                    alternating = False
                    break
                if j > i:
                    prev_up = measurements[j] > measurements[j - 1]
                    curr_up = measurements[j + 1] > measurements[j]
                    if prev_up == curr_up:
                        alternating = False
                        break
            if alternating:
                violations.append({
                    "rule": "14_points_alternating",
                    "start_index": i
                })
                i += 14
            else:
                i += 1
    
    return violations

input_line = sys.stdin.read().strip()
measurements = [float(x) for x in input_line.split(',')]
violations = detect_spc_violations(measurements)
result = {"rule_violations": violations}
print(json.dumps(result, separators=(',', ':')))