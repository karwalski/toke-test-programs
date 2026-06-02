import sys
import json
import math

def pelt_algorithm(data, penalty=10):
    n = len(data)
    if n <= 1:
        return []
    
    # Initialize
    F = [0] * (n + 1)
    cp = [-1] * (n + 1)
    
    for t in range(1, n + 1):
        min_cost = float('inf')
        best_tau = -1
        
        for tau in range(t):
            # Calculate cost for segment from tau to t
            segment = data[tau:t]
            segment_mean = sum(segment) / len(segment)
            cost = sum((x - segment_mean) ** 2 for x in segment)
            
            total_cost = F[tau] + cost + penalty
            
            if total_cost < min_cost:
                min_cost = total_cost
                best_tau = tau
        
        F[t] = min_cost
        cp[t] = best_tau
    
    # Backtrack to find change points
    change_points = []
    t = n
    while cp[t] != -1:
        if cp[t] > 0:
            change_points.append(cp[t])
        t = cp[t]
    
    change_points.reverse()
    return change_points

def get_segment_means(data, change_points):
    segments = []
    start = 0
    
    for cp in change_points:
        segments.append(data[start:cp])
        start = cp
    segments.append(data[start:])
    
    means = []
    for segment in segments:
        if segment:
            means.append(sum(segment) / len(segment))
    
    return means

# Read input
line = sys.stdin.readline().strip()
data = [float(x) for x in line.split(',')]

# Apply PELT algorithm
change_points = pelt_algorithm(data)
segment_means = get_segment_means(data, change_points)

# Output result
result = {
    "change_points": change_points,
    "segment_means": segment_means
}

print(json.dumps(result, separators=(',', ':')))