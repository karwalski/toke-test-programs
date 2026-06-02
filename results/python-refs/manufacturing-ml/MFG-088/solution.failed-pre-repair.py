import sys
import csv
import json
import math

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # First line contains prediction_x
    prediction_line = lines[0]
    prediction_x = float(prediction_line.split(',')[1])
    
    # Parse CSV data
    x_values = []
    y_values = []
    
    # Skip header line (x,y)
    for line in lines[2:]:
        parts = line.split(',')
        x_values.append(float(parts[0]))
        y_values.append(float(parts[1]))
    
    return prediction_x, x_values, y_values

def linear_regression(x_values, y_values):
    n = len(x_values)
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_xx = sum(x * x for x in x_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))
    
    # Calculate slope and intercept
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    
    return slope, intercept

def calculate_intervals(x_values, y_values, slope, intercept, prediction_x, confidence_level=0.95):
    n = len(x_values)
    
    # Calculate residual sum of squares
    y_pred = [slope * x + intercept for x in x_values]
    rss = sum((y - yp) ** 2 for y, yp in zip(y_values, y_pred))
    
    # Standard error
    mse = rss / (n - 2)
    se = math.sqrt(mse)
    
    # Calculate prediction
    prediction = slope * prediction_x + intercept
    
    # Calculate standard errors for intervals
    x_mean = sum(x_values) / n
    sxx = sum((x - x_mean) ** 2 for x in x_values)
    
    # Standard error for confidence interval
    se_conf = se * math.sqrt(1/n + (prediction_x - x_mean)**2 / sxx)
    
    # Standard error for prediction interval
    se_pred = se * math.sqrt(1 + 1/n + (prediction_x - x_mean)**2 / sxx)
    
    # t-value for 95% confidence (approximation for small samples)
    # Using t-distribution critical value for df = n-2
    t_value = 2.776  # for df=3, 95% confidence
    
    # Calculate intervals
    conf_margin = t_value * se_conf
    pred_margin = t_value * se_pred
    
    confidence_interval = [prediction - conf_margin, prediction + conf_margin]
    prediction_interval = [prediction - pred_margin, prediction + pred_margin]
    
    return prediction, confidence_interval, prediction_interval

def main():
    prediction_x, x_values, y_values = read_input()
    
    slope, intercept = linear_regression(x_values, y_values)
    prediction, confidence_interval, prediction_interval = calculate_intervals(
        x_values, y_values, slope, intercept, prediction_x
    )
    
    result = {
        "prediction": round(prediction, 1),
        "confidence_interval": [round(ci, 1) for ci in confidence_interval],
        "prediction_interval": [round(pi, 1) for pi in prediction_interval]
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()