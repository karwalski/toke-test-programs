import sys
import csv
import json

D3_FACTORS = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223}
D4_FACTORS = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777}

reader = csv.reader(sys.stdin)
ranges = []
subgroup_size = 0

for row in reader:
    values = [float(x) for x in row]
    if not values:
        continue
    subgroup_size = len(values)
    ranges.append(max(values) - min(values))

r_bar = sum(ranges) / len(ranges)

d3 = D3_FACTORS.get(subgroup_size, 0)
d4 = D4_FACTORS.get(subgroup_size, 2.574)

ucl = d4 * r_bar
lcl = d3 * r_bar
if lcl < 0:
    lcl = 0

result = {
    "r_bar": round(r_bar, 2),
    "ucl": round(ucl, 2),
    "lcl": round(lcl, 2)
}

print(json.dumps(result, separators=(',', ':')))