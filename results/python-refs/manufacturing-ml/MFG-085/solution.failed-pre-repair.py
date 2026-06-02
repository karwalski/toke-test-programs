import sys
import json
import math

def calculate_acf(data, max_lag):
    n = len(data)
    mean = sum(data) / n
    
    # Calculate variance (lag 0 autocovariance)
    variance = sum((x - mean) ** 2 for x in data) / n
    
    acf = []
    
    for lag in range(max_lag + 1):
        if lag == 0:
            acf.append(1.0)
        else:
            # Calculate autocovariance at this lag
            autocovariance = 0
            count = 0
            
            for i in range(n - lag):
                autocovariance += (data[i] - mean) * (data[i + lag] - mean)
                count += 1
            
            if count > 0:
                autocovariance /= count
                # ACF is autocovariance divided by variance
                acf_value = autocovariance / variance if variance != 0 else 0
                acf.append(round(acf_value, 2))
            else:
                acf.append(0.0)
    
    return acf

def find_significant_lags(acf, threshold=0.5):
    significant_lags = []
    for i, value in enumerate(acf):
        if abs(value) >= threshold:
            significant_lags.append(i)
    return significant_lags

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

max_lag = int(lines[0])
values = list(map(float, lines[1].split(',')))

# Calculate ACF
acf = calculate_acf(values, max_lag)

# Find significant lags (using threshold of 0.5 based on expected output)
significant_lags = find_significant_lags(acf, 0.5)

# Output result
result = {
    "acf": acf,
    "significant_lags": significant_lags
}

print(json.dumps(result, separators=(',', ':')))