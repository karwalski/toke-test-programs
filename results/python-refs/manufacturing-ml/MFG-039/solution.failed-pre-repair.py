import sys
import csv
import json
from io import StringIO

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    # Parse CSV data
    csv_reader = csv.DictReader(StringIO(input_data))
    
    # Group events by machine
    machines = {}
    
    for row in csv_reader:
        machine = row['machine']
        start_time = int(row['start_time'])
        end_time = int(row['end_time'])
        reason = row['reason']
        
        if machine not in machines:
            machines[machine] = []
        
        machines[machine].append({
            'start_time': start_time,
            'end_time': end_time,
            'reason': reason,
            'duration': end_time - start_time
        })
    
    # Calculate metrics for each machine
    result_machines = []
    
    for machine_name, events in machines.items():
        # Sort events by start time
        events.sort(key=lambda x: x['start_time'])
        
        # Calculate total downtime
        total_downtime = sum(event['duration'] for event in events)
        
        # Calculate MTBF (Mean Time Between Failures)
        # MTBF = total uptime / number of failure periods
        if len(events) > 1:
            # Time between failures
            uptime_periods = []
            for i in range(1, len(events)):
                uptime = events[i]['start_time'] - events[i-1]['end_time']
                uptime_periods.append(uptime)
            
            mtbf = sum(uptime_periods) / len(uptime_periods) if uptime_periods else 0
        else:
            mtbf = 0
        
        # Calculate MTTR (Mean Time To Repair)
        # MTTR = total downtime / number of events
        mttr = total_downtime / len(events) if events else 0
        
        result_machines.append({
            'machine': machine_name,
            'total_downtime': int(total_downtime),
            'mtbf': int(mtbf),
            'mttr': int(mttr)
        })
    
    # Create output JSON
    output = {
        'machines': result_machines
    }
    
    # Print JSON output without extra whitespace
    print(json.dumps(output, separators=(',', ':')))

if __name__ == '__main__':
    main()