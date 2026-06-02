import sys
import json
import math

def mann_kendall_test(data):
    """
    Perform Mann-Kendall test for monotonic trend detection.
    
    Returns:
        s_statistic: The Mann-Kendall S statistic
        p_value: Two-tailed p-value
        trend_present: Boolean indicating if trend is present
        direction: "increasing", "decreasing", or "no trend"
    """
    n = len(data)
    
    # Calculate S statistic
    s = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            if data[j] > data[i]:
                s += 1
            elif data[j] < data[i]:
                s -= 1
    
    # Calculate variance
    var_s = n * (n - 1) * (2 * n + 5) / 18
    
    # Calculate standardized test statistic Z
    if s > 0:
        z = (s - 1) / math.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / math.sqrt(var_s)
    else:
        z = 0
    
    # Calculate two-tailed p-value using normal distribution
    # Complementary error function approximation for standard normal CDF
    def normal_cdf(x):
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    p_value = 2 * (1 - normal_cdf(abs(z)))
    
    # Determine trend presence (typically alpha = 0.05)
    alpha = 0.05
    trend_present = p_value < alpha
    
    # Determine direction
    if trend_present:
        if s > 0:
            direction = "increasing"
        else:
            direction = "decreasing"
    else:
        direction = "no trend"
    
    return s, p_value, trend_present, direction

# Read input from stdin
input_line = sys.stdin.read().strip()
data = [float(x) for x in input_line.split(',')]

# Perform Mann-Kendall test
s_stat, p_val, trend_present, direction = mann_kendall_test(data)

# Format output as JSON
result = {
    "s_statistic": s_stat,
    "p_value": p_val,
    "trend_present": trend_present,
    "direction": direction
}

# Print JSON output
print(json.dumps(result, separators=(',', ':')))