import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
alarm_data = {}

for row in reader:
    alarm_id = row['alarm_id']
    duration = int(row['duration_sec'])
    
    if alarm_id not in alarm_data:
        alarm_data[alarm_id] = {'count': 0, 'total_duration': 0}
    
    alarm_data[alarm_id]['count'] += 1
    alarm_data[alarm_id]['total_duration'] += duration

# Calculate stats and determine nuisance alarms
alarms = []
for alarm_id, data in alarm_data.items():
    count = data['count']
    avg_duration = data['total_duration'] / count
    # Consider an alarm nuisance if it occurs more than 3 times
    nuisance = count > 3
    
    alarms.append({
        'alarm_id': alarm_id,
        'count': count,
        'avg_duration': avg_duration,
        'nuisance': nuisance
    })

# Sort by alarm_id for consistent output
alarms.sort(key=lambda x: x['alarm_id'])

# Output JSON
result = {'alarms': alarms}
print(json.dumps(result, separators=(',', ':')))