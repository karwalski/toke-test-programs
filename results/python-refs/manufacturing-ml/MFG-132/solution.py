import csv
import json
import sys
import math

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
for row in reader:
    total_hours = float(row['total_hours'])
    num_failures = int(row['num_failures'])
    mission_time = float(row['mission_time'])
    
    # Calculate metrics assuming exponential failure distribution
    failure_rate = num_failures / total_hours
    mtbf = total_hours / num_failures
    reliability_at_mission = math.exp(-failure_rate * mission_time)
    
    # Format output to match expected precision
    result = {
        "failure_rate": round(failure_rate, 4),
        "mtbf": int(mtbf),
        "reliability_at_mission": round(reliability_at_mission, 2)
    }
    
    print(json.dumps(result, separators=(',', ':')))