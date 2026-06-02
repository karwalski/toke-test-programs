import csv
import json
import sys
import math

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
dimensions = list(reader)

# Calculate totals
total_nominal = 0
total_tolerance = 0
sum_of_squares = 0

for dim in dimensions:
    nominal = float(dim['nominal'])
    tolerance = float(dim['tolerance'])
    
    total_nominal += nominal
    total_tolerance += tolerance
    sum_of_squares += tolerance * tolerance

# Calculate results
worst_case_min = total_nominal - total_tolerance
worst_case_max = total_nominal + total_tolerance
rss_tolerance = math.sqrt(sum_of_squares)

# Output JSON
result = {
    "total_nominal": total_nominal,
    "worst_case_min": worst_case_min,
    "worst_case_max": worst_case_max,
    "rss_tolerance": round(rss_tolerance, 2)
}

print(json.dumps(result, separators=(',', ':')))