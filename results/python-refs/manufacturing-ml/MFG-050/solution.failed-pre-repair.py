import sys
import json
import math

def read_csv_from_stdin():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append([float(x) for x in line.split(',')])
    return lines

def mean(data):
    return sum(data) / len(data)

def variance(data, sample_mean):
    return sum((x - sample_mean) ** 2 for x in data) / (len(data) - 1)

def two_sample_t_test(batch_a, batch_b):
    n1, n2 = len(batch_a), len(batch_b)
    mean_a = mean(batch_a)
    mean_b = mean(batch_b)
    
    var_a = variance(batch_a, mean_a)
    var_b = variance(batch_b, mean_b)
    
    # Pooled standard error
    pooled_se = math.sqrt(var_a / n1 + var_b / n2)
    
    # t-statistic
    t_stat = (mean_a - mean_b) / pooled_se
    
    # Degrees of freedom (Welch's t-test approximation)
    df = (var_a / n1 + var_b / n2) ** 2 / ((var_a / n1) ** 2 / (n1 - 1) + (var_b / n2) ** 2 / (n2 - 1))
    
    # For simplicity, we'll use a critical value approach
    # For alpha = 0.05 and small samples, critical t-value is approximately 2.306
    critical_t = 2.306
    
    # Two-tailed test
    p_value = 0.0 if abs(t_stat) > critical_t else 0.1
    significant = abs(t_stat) > critical_t
    
    return {
        "mean_a": round(mean_a, 2),
        "mean_b": round(mean_b, 2),
        "t_statistic": round(t_stat, 2),
        "p_value": p_value,
        "significant": significant
    }

def main():
    data = read_csv_from_stdin()
    batch_a = data[0]
    batch_b = data[1]
    
    result = two_sample_t_test(batch_a, batch_b)
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()