import csv
import sys
import json
import math

# Read CSV data from stdin
reader = csv.DictReader(sys.stdin)
data = []
for row in reader:
    sample_size = int(row['sample_size'])
    defectives = int(row['defectives'])
    data.append((sample_size, defectives))

# Calculate p_bar (average proportion defective)
total_defectives = sum(defectives for _, defectives in data)
total_sample_size = sum(sample_size for sample_size, _ in data)
p_bar = total_defectives / total_sample_size

# Calculate control limits
# For p-chart: UCL/LCL = p_bar ± 3 * sqrt(p_bar * (1 - p_bar) / n)
# Assuming constant sample size for control limits
n = data[0][0]  # Use first sample size
std_error = math.sqrt(p_bar * (1 - p_bar) / n)
ucl = p_bar + 3 * std_error
lcl = max(0, p_bar - 3 * std_error)  # LCL cannot be negative

# Find out of control points
out_of_control = []
for i, (sample_size, defectives) in enumerate(data):
    proportion = defectives / sample_size
    if proportion > ucl or proportion < lcl:
        out_of_control.append(i)

# Format output
result = {
    "p_bar": round(p_bar, 3),
    "ucl": round(ucl, 2),
    "lcl": round(lcl, 1),
    "out_of_control": out_of_control
}

print(json.dumps(result, separators=(',', ':')))