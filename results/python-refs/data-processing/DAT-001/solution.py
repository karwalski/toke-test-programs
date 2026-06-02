import csv
import json
import sys

reader = csv.reader(sys.stdin)
for row in reader:
    print(json.dumps(row, separators=(',', ':')))