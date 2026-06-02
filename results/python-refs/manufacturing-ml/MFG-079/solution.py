import csv
import json
import sys
import statistics
import math

def calculate_spc_metrics(values, lsl, usl):
    if len(values) < 2:
        return None, None, None, None, 0
    
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    
    # Calculate Cp
    cp = (usl - lsl) / (6 * std) if std > 0 else float('inf')
    
    # Calculate Cpk
    cpu = (usl - mean) / (3 * std) if std > 0 else float('inf')
    cpl = (mean - lsl) / (3 * std) if std > 0 else float('inf')
    cpk = min(cpu, cpl)
    
    # Count out of control (outside LSL/USL)
    out_of_control = sum(1 for v in values if v < lsl or v > usl)
    
    return mean, std, cp, cpk, out_of_control

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
data = {}

for row in reader:
    param = row['parameter']
    value = float(row['value'])
    lsl = float(row['lsl'])
    usl = float(row['usl'])
    
    if param not in data:
        data[param] = {'values': [], 'lsl': lsl, 'usl': usl}
    
    data[param]['values'].append(value)

# Calculate metrics for each parameter
parameters = []
for param_name, param_data in data.items():
    values = param_data['values']
    lsl = param_data['lsl']
    usl = param_data['usl']
    
    mean, std, cp, cpk, out_of_control = calculate_spc_metrics(values, lsl, usl)
    
    parameters.append({
        'name': param_name,
        'mean': round(mean, 2),
        'std': round(std, 2),
        'cp': round(cp, 2),
        'cpk': round(cpk, 2),
        'out_of_control': out_of_control
    })

# Output JSON
result = {'parameters': parameters}
print(json.dumps(result, separators=(',', ':')))