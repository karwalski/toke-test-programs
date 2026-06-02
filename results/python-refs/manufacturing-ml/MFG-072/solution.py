import sys
import json
import math
from math import comb

def binomial_probability(n, k, p):
    """Calculate binomial probability P(X <= k) for n trials with probability p"""
    prob = 0
    for i in range(k + 1):
        prob += comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return prob

def main():
    # Read input from stdin
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse CSV input
    sample_size = None
    accept_number = None
    
    for line in lines:
        if line.startswith('sample_size,'):
            sample_size = int(line.split(',')[1])
        elif line.startswith('accept_number,'):
            accept_number = int(line.split(',')[1])
    
    # Calculate OC curve points for standard p values
    p_values = [0.01, 0.05, 0.1]
    oc_points = []
    
    for p in p_values:
        pa = binomial_probability(sample_size, accept_number, p)
        oc_points.append({"p": p, "pa": round(pa, 2)})
    
    # Output JSON
    result = {"oc_points": oc_points}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()