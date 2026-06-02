import sys
import json
import csv

def read_data():
    data = []
    reader = csv.DictReader(sys.stdin)
    for row in reader:
        x = float(row['x'])
        y = float(row['y'])
        data.append((x, y))
    return data

def interpolate_quality(x, data):
    if x <= data[0][0]:
        return data[0][1]
    if x >= data[-1][0]:
        return data[-1][1]
    for i in range(len(data) - 1):
        x1, y1 = data[i]
        x2, y2 = data[i + 1]
        if x1 <= x <= x2:
            t = (x - x1) / (x2 - x1)
            return y1 + t * (y2 - y1)
    return data[-1][1]

def numerical_gradient(x, data, h=0.01):
    y_plus = interpolate_quality(x + h, data)
    y_minus = interpolate_quality(x - h, data)
    return (y_plus - y_minus) / (2 * h)

def gradient_descent(data):
    x_min = min(p[0] for p in data)
    x_max = max(p[0] for p in data)
    x = (x_min + x_max) / 2
    
    learning_rate = 0.01
    threshold = 0.001
    max_iterations = 1000
    
    for iteration in range(1, max_iterations + 1):
        grad = numerical_gradient(x, data)
        x_new = x + learning_rate * grad
        x_new = max(x_min, min(x_max, x_new))
        
        if abs(x_new - x) < threshold:
            x = x_new
            return x, interpolate_quality(x, data), iteration
        x = x_new
    
    return x, interpolate_quality(x, data), max_iterations

def main():
    data = read_data()
    data.sort()
    optimal_x, optimal_y, iterations = gradient_descent(data)
    optimal_x_r = round(optimal_x, 6)
    if abs(optimal_x_r - round(optimal_x_r)) < 1e-4:
        optimal_x_r = float(round(optimal_x_r))
    optimal_y_r = round(optimal_y, 6)
    if abs(optimal_y_r - round(optimal_y_r)) < 1e-4:
        optimal_y_r = float(round(optimal_y_r))
    result = {
        "optimal_x": optimal_x_r,
        "optimal_y": optimal_y_r,
        "iterations": iterations
    }
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()