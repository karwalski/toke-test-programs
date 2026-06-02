import sys
import json
import math

def main():
    measurements = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            measurements.append(float(line))
    
    if len(measurements) == 0:
        print('{"violations":[]}')
        return
    
    n = len(measurements)
    mean = sum(measurements) / n
    
    # Use moving range estimate for sigma (typical for control charts)
    # This avoids inflating sigma due to the outlier itself
    if n >= 2:
        moving_ranges = [abs(measurements[i] - measurements[i-1]) for i in range(1, n)]
        mr_bar = sum(moving_ranges) / len(moving_ranges)
        # d2 for n=2 is 1.128
        sigma_mr = mr_bar / 1.128
    else:
        sigma_mr = 0
    
    # Also compute sample std
    if n > 1:
        variance = sum((x - mean) ** 2 for x in measurements) / (n - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0
    
    # Use the smaller (moving range based) to detect outliers robustly
    sigma = sigma_mr if sigma_mr > 0 else std_dev
    
    ucl = mean + 3 * sigma
    lcl = mean - 3 * sigma
    
    violations = []
    for i, value in enumerate(measurements):
        if value > ucl or value < lcl:
            violations.append({"rule": "1_beyond_3sigma", "index": i})
    
    # Rule 2: 9 consecutive points on same side of mean
    if n >= 9:
        for i in range(8, n):
            window = measurements[i-8:i+1]
            if all(x > mean for x in window) or all(x < mean for x in window):
                violations.append({"rule": "2_nine_same_side", "index": i})
    
    # Rule 3: 6 consecutive increasing or decreasing
    if n >= 6:
        for i in range(5, n):
            window = measurements[i-5:i+1]
            inc = all(window[j] < window[j+1] for j in range(5))
            dec = all(window[j] > window[j+1] for j in range(5))
            if inc or dec:
                violations.append({"rule": "3_six_trend", "index": i})
    
    # Rule 4: 14 consecutive alternating
    if n >= 14:
        for i in range(13, n):
            window = measurements[i-13:i+1]
            alt = True
            for j in range(13):
                diff1 = window[j+1] - window[j]
                if j > 0:
                    diff0 = window[j] - window[j-1]
                    if diff0 * diff1 >= 0:
                        alt = False
                        break
            if alt:
                violations.append({"rule": "4_fourteen_alternating", "index": i})
    
    result = {"violations": violations}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()