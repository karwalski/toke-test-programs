import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
machines = []

for row in reader:
    machine = row['machine']
    planned_time = float(row['planned_time'])
    run_time = float(row['run_time'])
    ideal_cycle = float(row['ideal_cycle'])
    total_count = int(row['total_count'])
    good_count = int(row['good_count'])
    
    # Calculate OEE components
    availability = run_time / planned_time
    ideal_production_time = total_count * ideal_cycle
    performance = ideal_production_time / run_time
    quality = good_count / total_count
    oee = availability * performance * quality
    
    machines.append({
        "machine": machine,
        "availability": round(availability, 2),
        "performance": round(performance, 2),
        "quality": round(quality, 2),
        "oee": round(oee, 2)
    })

# Output JSON
result = {"machines": machines}
print(json.dumps(result, separators=(',', ':')))