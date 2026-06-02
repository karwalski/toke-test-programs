import sys
import json
import math

def main():
    # Read measurements from stdin
    measurements = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            measurements.append(float(line))
    
    if len(measurements) == 0:
        print('{"violations":[]}')
        return
    
    # Calculate mean and standard deviation
    mean = sum(measurements) / len(measurements)
    
    # Calculate sample standard deviation
    if len(measurements) <= 1:
        std_dev = 0
    else:
        variance = sum((x - mean) ** 2 for x in measurements) / (len(measurements) - 1)
        std_dev = math.sqrt(variance)
    
    # Calculate control limits (3-sigma)
    ucl = mean + 3 * std_dev
    lcl = mean - 3 * std_dev
    
    # Check for Western Electric Rule 1: Point beyond 3-sigma
    violations = []
    for i, value in enumerate(measurements):
        if value > ucl or value < lcl:
            violations.append({"rule": "1_beyond_3sigma", "index": i})
    
    # Output result
    result = {"violations": violations}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()