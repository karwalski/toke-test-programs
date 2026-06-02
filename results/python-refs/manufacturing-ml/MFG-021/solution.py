import sys
import json

lines = sys.stdin.read().strip().split('\n')
data_lines = lines[1:]

x_values = []
y_values = []

for line in data_lines:
    x, y = line.split(',')
    x_values.append(float(x))
    y_values.append(float(y))

n = len(x_values)
x_mean = sum(x_values) / n
y_mean = sum(y_values) / n

numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))

slope = numerator / denominator
intercept = y_mean - slope * x_mean

y_pred = [slope * x + intercept for x in x_values]
ss_res = sum((y_values[i] - y_pred[i]) ** 2 for i in range(n))
ss_tot = sum((y_values[i] - y_mean) ** 2 for i in range(n))
r_squared = 1 - (ss_res / ss_tot)

slope_r = round(slope, 2)
intercept_r = round(intercept, 2)
r_squared_r = round(r_squared, 2)

def fmt(v):
    if v == int(v):
        return f"{v:.1f}"
    return str(v)

out = '{"slope":' + fmt(slope_r) + ',"intercept":' + fmt(intercept_r) + ',"r_squared":' + fmt(r_squared_r) + '}'
print(out)