import sys
import csv
import json

# Constants for range chart control limits (D3 and D4 factors)
# These are standard factors based on subgroup size
D3_FACTORS = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223}
D4_FACTORS = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777}

# Read CSV data from stdin
reader = csv.reader(sys.stdin)
ranges = []

for row in reader:
    # Convert string values to float
    values = [float(x) for x in row]
    # Calculate range (max - min) for this subgroup
    subgroup_range = max(values) - min(values)
    ranges.append(subgroup_range)

# Calculate R-bar (average range)
r_bar = sum(ranges) / len(ranges)

# Get subgroup size from first row
subgroup_size = len(ranges) if len(ranges) <= 10 else 10

# Get control limit factors
d3 = D3_FACTORS.get(subgroup_size, 0)
d4 = D4_FACTORS.get(subgroup_size, 2.574)  # default to n=3 if not found

# Calculate control limits
ucl = d4 * r_bar
lcl = d3 * r_bar

# Create output dictionary
result = {
    "r_bar": round(r_bar, 2),
    "ucl": round(ucl, 2),
    "lcl": round(lcl, 1)
}

# Output as JSON
print(json.dumps(result, separators=(',', ':')))