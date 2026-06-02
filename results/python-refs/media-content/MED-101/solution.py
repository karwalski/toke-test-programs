import csv
import json
import sys

reader = csv.DictReader(sys.stdin)
data = list(reader)
print(json.dumps(data, separators=(',', ':')))