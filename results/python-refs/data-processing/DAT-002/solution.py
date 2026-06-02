import csv
import json
import sys

reader = csv.DictReader(sys.stdin)
data = [dict(row) for row in reader]

# Custom pretty print: array indented, objects on single line
lines = ["["]
for i, obj in enumerate(data):
    line = "  " + json.dumps(obj)
    if i < len(data) - 1:
        line += ","
    lines.append(line)
lines.append("]")
print("\n".join(lines))