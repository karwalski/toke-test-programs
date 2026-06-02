import sys
import statistics

def detect_outliers_iqr(values, threshold):
    outliers = []
    
    # Calculate Q1, Q3, and IQR
    q1 = statistics.quantiles(values, n=4)[0]
    q3 = statistics.quantiles(values, n=4)[2]
    iqr = q3 - q1
    
    # Calculate bounds
    lower_bound = q1 - threshold * iqr
    upper_bound = q3 + threshold * iqr
    
    # Find outliers
    for i, value in enumerate(values):
        if value < lower_bound or value > upper_bound:
            outliers.append((i, value))
    
    return outliers

def detect_outliers_zscore(values, threshold):
    outliers = []
    
    # Calculate mean and standard deviation
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    
    # Find outliers
    for i, value in enumerate(values):
        z_score = abs((value - mean) / stdev)
        if z_score > threshold:
            outliers.append((i, value))
    
    return outliers

# Read input
method = input().strip()
threshold = float(input().strip())
values_line = input().strip()
values = list(map(float, values_line.split()))

# Detect outliers based on method
if method == "iqr":
    outliers = detect_outliers_iqr(values, threshold)
elif method == "zscore":
    outliers = detect_outliers_zscore(values, threshold)

# Output results
for index, value in outliers:
    if value == int(value):
        print(f"Index {index}: {int(value)} (outlier)")
    else:
        print(f"Index {index}: {value} (outlier)")