import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP

def r2(x):
    return float(Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

reader = csv.DictReader(sys.stdin)
machines = []

for row in reader:
    machine = row['machine']
    planned_time = float(row['planned_time'])
    run_time = float(row['run_time'])
    ideal_cycle = float(row['ideal_cycle'])
    total_count = int(row['total_count'])
    good_count = int(row['good_count'])
    
    availability = run_time / planned_time
    ideal_production_time = total_count * ideal_cycle
    performance = ideal_production_time / run_time
    quality = good_count / total_count
    oee = availability * performance * quality
    
    machines.append({
        "machine": machine,
        "availability": r2(availability),
        "performance": r2(performance),
        "quality": r2(quality),
        "oee": r2(oee)
    })

result = {"machines": machines}
print(json.dumps(result, separators=(',', ':')))