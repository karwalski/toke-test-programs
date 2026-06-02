import sys
import json
import csv
import math

# Read CSV data from stdin
csv_reader = csv.reader(sys.stdin)
subgroups = []

for row in csv_reader:
    subgroup = [float(x) for x in row]
    subgroups.append(subgroup)

# Calculate subgroup means
subgroup_means = []
for subgroup in subgroups:
    mean = sum(subgroup) / len(subgroup)
    subgroup_means.append(mean)

# Calculate X-bar (mean of subgroup means)
x_bar = sum(subgroup_means) / len(subgroup_means)

# Calculate subgroup ranges
subgroup_ranges = []
for subgroup in subgroups:
    range_val = max(subgroup) - min(subgroup)
    subgroup_ranges.append(range_val)

# Calculate R-bar (mean of subgroup ranges)
r_bar = sum(subgroup_ranges) / len(subgroup_ranges)

# Get sample size (assuming all subgroups have same size)
n = len(subgroups[0])

# A2 factors for different sample sizes
A2_factors = {
    2: 1.880,
    3: 1.023,
    4: 0.729,
    5: 0.577,
    6: 0.483,
    7: 0.419,
    8: 0.373,
    9: 0.337,
    10: 0.308
}

A2 = A2_factors[n]

# Calculate control limits
ucl = x_bar + A2 * r_bar
lcl = x_bar - A2 * r_bar

# Output JSON
result = {
    "x_bar": round(x_bar, 2),
    "ucl": round(ucl, 2),
    "lcl": round(lcl, 2)
}

print(json.dumps(result, separators=(',', ':')))