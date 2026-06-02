import sys
import json
import csv
from io import StringIO

def read_data():
    data = []
    reader = csv.DictReader(sys.stdin)
    for row in reader:
        x = float(row['x'])
        y = float(row['y'])
        data.append((x, y))
    return data

def interpolate_quality(x, data):
    # Linear interpolation between data points
    if x <= data[0][0]:
        return data[0][1]
    if x >= data[-1][0]:
        return data[-1][1]
    
    for i in range(len(data) - 1):
        x1, y1 = data[i]
        x2, y2 = data[i + 1]
        if x1 <= x <= x2:
            # Linear interpolation
            t = (x - x1) / (x2 - x1)
            return y1 + t * (y2 - y1)
    
    return data[-1][1]

def numerical_gradient(x, data, h=0.01):
    # Numerical gradient using finite differences
    y_plus = interpolate_quality(x + h, data)
    y_minus = interpolate_quality(x - h, data)
    return (y_plus - y_minus) / (2 * h)

def gradient_descent(data):
    # Initialize at midpoint
    x_min = min(point[0] for point in data)
    x_max = max(point[0] for point in data)
    x = (x_min + x_max) / 2
    
    learning_rate = 0.1
    max_iterations = 100
    tolerance = 1e-6
    
    for iteration in range(max_iterations):
        grad = numerical_gradient(x, data)
        x_new = x + learning_rate * grad  # Move in direction of positive gradient (maximizing)
        
        # Keep x within bounds
        x_new = max(x_min, min(x_max, x_new))
        
        # Check for convergence
        if abs(x_new - x) < tolerance:
            return x_new, interpolate_quality(x_new, data), iteration + 1
        
        x = x_new
    
    return x, interpolate_quality(x, data), max_iterations

def main():
    data = read_data()
    data.sort()  # Sort by x values
    
    optimal_x, optimal_y, iterations = gradient_descent(data)
    
    result = {
        "optimal_x": float(optimal_x),
        "optimal_y": float(optimal_y),
        "iterations": iterations
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()