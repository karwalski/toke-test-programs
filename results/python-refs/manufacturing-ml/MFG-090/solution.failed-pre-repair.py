import sys
import csv
import json
import math

def read_csv_data():
    reader = csv.DictReader(sys.stdin)
    x_vals = []
    y_vals = []
    for row in reader:
        x_vals.append(float(row['x']))
        y_vals.append(float(row['y']))
    return x_vals, y_vals

def linear_regression(x_vals, y_vals):
    n = len(x_vals)
    sum_x = sum(x_vals)
    sum_y = sum(y_vals)
    sum_xy = sum(x * y for x, y in zip(x_vals, y_vals))
    sum_x2 = sum(x * x for x in x_vals)
    
    # Calculate slope and intercept
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    
    return slope, intercept

def calculate_residuals(x_vals, y_vals, slope, intercept):
    residuals = []
    for x, y in zip(x_vals, y_vals):
        predicted = slope * x + intercept
        residual = y - predicted
        residuals.append(round(residual, 2))
    return residuals

def shapiro_wilk_test(residuals):
    # Simple normality test - for small samples, check if residuals follow normal pattern
    n = len(residuals)
    if n < 3:
        return True
    
    # Calculate mean and std dev
    mean_res = sum(residuals) / n
    var_res = sum((r - mean_res) ** 2 for r in residuals) / (n - 1)
    std_res = math.sqrt(var_res)
    
    # Simple check: if all residuals are within 2 standard deviations, consider normal
    if std_res == 0:
        return True
    
    for r in residuals:
        if abs(r - mean_res) > 2 * std_res:
            return False
    return True

def durbin_watson_test(residuals):
    # Test for autocorrelation
    if len(residuals) < 2:
        return False
    
    diff_sum = sum((residuals[i] - residuals[i-1]) ** 2 for i in range(1, len(residuals)))
    residual_sum = sum(r ** 2 for r in residuals)
    
    if residual_sum == 0:
        return False
    
    dw_stat = diff_sum / residual_sum
    
    # DW statistic around 2 indicates no autocorrelation
    # Values significantly different from 2 indicate autocorrelation
    return abs(dw_stat - 2) > 0.5

def main():
    x_vals, y_vals = read_csv_data()
    slope, intercept = linear_regression(x_vals, y_vals)
    residuals = calculate_residuals(x_vals, y_vals, slope, intercept)
    
    is_normal = shapiro_wilk_test(residuals)
    is_autocorrelated = durbin_watson_test(residuals)
    
    result = {
        "residuals": residuals,
        "normal": is_normal,
        "autocorrelated": is_autocorrelated
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()