import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)

out_of_spec_count = 0

for row in reader:
    measurement = float(row['measurement'])
    lsl = float(row['lsl'])
    usl = float(row['usl'])
    
    if measurement < lsl or measurement > usl:
        out_of_spec_count += 1

in_spec = out_of_spec_count == 0

result = {
    "in_spec": in_spec,
    "out_of_spec_count": out_of_spec_count
}

print(json.dumps(result, separators=(',', ':')))