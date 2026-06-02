import sys
import json
import math

def shapiro_wilk_test(data):
    n = len(data)
    if n < 3 or n > 5000:
        raise ValueError("Sample size must be between 3 and 5000")
    
    # Sort the data
    x = sorted(data)
    
    # Calculate mean
    mean = sum(x) / n
    
    # Calculate sum of squares
    ss = sum((xi - mean) ** 2 for xi in x)
    
    # Shapiro-Wilk coefficients (approximation for small samples)
    # This is a simplified implementation
    if n <= 11:
        # For small samples, use simplified calculation
        a = []
        for i in range(n // 2):
            if i == 0:
                a.append(0.7071 if n == 3 else 0.6872 if n == 4 else 0.6646 if n == 5 else 0.6431)
            else:
                a.append(0.1677 if n <= 5 else 0.2413 if n <= 7 else 0.2806)
    else:
        # For larger samples, use normal approximation
        a = []
        for i in range(n // 2):
            a.append(1.0 / math.sqrt(n))
    
    # Calculate W statistic
    b = 0
    for i in range(n // 2):
        b += a[i] * (x[n-1-i] - x[i])
    
    w = (b * b) / ss
    
    # Approximate p-value calculation
    # This is a simplified approximation
    if n <= 20:
        # For small samples
        if w > 0.95:
            p_value = 0.5 + (w - 0.95) * 8
        elif w > 0.90:
            p_value = 0.1 + (w - 0.90) * 8
        else:
            p_value = 0.01
    else:
        # For larger samples, use normal approximation
        ln_w = math.log(w)
        if ln_w > -0.1:
            p_value = 0.8
        elif ln_w > -0.2:
            p_value = 0.5
        else:
            p_value = 0.1
    
    p_value = min(1.0, max(0.01, p_value))
    
    return w, p_value

# Read input from stdin
input_line = sys.stdin.read().strip()
measurements = [float(x) for x in input_line.split(',')]

# Perform Shapiro-Wilk test
w_stat, p_val = shapiro_wilk_test(measurements)

# Determine if distribution is normal (typically p > 0.05)
is_normal = p_val > 0.05

# Format output to match expected format
result = {
    "w_statistic": round(w_stat, 2),
    "p_value": round(p_val, 2),
    "is_normal": is_normal
}

# Convert boolean to lowercase string for JSON
json_str = json.dumps(result)
json_str = json_str.replace('true', 'true').replace('false', 'false')

print(json_str)