import csv
import json
import sys
from functools import reduce
import operator

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
yields = []

for row in reader:
    yields.append(float(row['yield']))

# Calculate rolled throughput yield (product of all yields)
rty = reduce(operator.mul, yields, 1)

# Round to 2 decimal places and output as JSON
result = {"rty": round(rty, 2)}
print(json.dumps(result, separators=(',', ':')))