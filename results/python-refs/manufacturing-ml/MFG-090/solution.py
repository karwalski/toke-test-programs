import sys
import csv
import json
import math

def main():
    reader = csv.DictReader(sys.stdin)
    x_vals = []
    y_vals = []
    for row in reader:
        x_vals.append(float(row['x']))
        y_vals.append(float(row['y']))
    
    n = len(x_vals)
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n
    
    num = sum((x_vals[i] - mean_x) * (y_vals[i] - mean_y) for i in range(n))
    den = sum((x_vals[i] - mean_x) ** 2 for i in range(n))
    
    slope = num / den
    intercept = mean_y - slope * mean_x
    
    residuals = []
    for x, y in zip(x_vals, y_vals):
        predicted = slope * x + intercept
        residuals.append(round(y - predicted, 2))
    
    # Normality test
    is_normal = True
    if n >= 3:
        mean_res = sum(residuals) / n
        var_res = sum((r - mean_res) ** 2 for r in residuals) / (n - 1) if n > 1 else 0
        std_res = math.sqrt(var_res)
        if std_res > 0:
            for r in residuals:
                if abs(r - mean_res) > 2 * std_res:
                    is_normal = False
                    break
    
    # Durbin-Watson
    is_autocorrelated = False
    if len(residuals) >= 2:
        diff_sum = sum((residuals[i] - residuals[i-1]) ** 2 for i in range(1, len(residuals)))
        residual_sum = sum(r ** 2 for r in residuals)
        if residual_sum > 0:
            dw_stat = diff_sum / residual_sum
            # DW between ~1.5 and 2.5 indicates no autocorrelation
            if dw_stat < 1.0 or dw_stat > 3.0:
                is_autocorrelated = True
    
    result = {
        "residuals": residuals,
        "normal": is_normal,
        "autocorrelated": is_autocorrelated
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()