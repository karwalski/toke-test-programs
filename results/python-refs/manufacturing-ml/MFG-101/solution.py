import sys
import json

def process_streaming_measurements():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse control limits
    ucl = None
    lcl = None
    cl = None
    
    i = 0
    while i < len(lines) and (ucl is None or lcl is None or cl is None):
        line = lines[i]
        if line.startswith('ucl,'):
            ucl = float(line.split(',')[1])
        elif line.startswith('lcl,'):
            lcl = float(line.split(',')[1])
        elif line.startswith('cl,'):
            cl = float(line.split(',')[1])
        i += 1
    
    # Parse measurements
    measurements = []
    for j in range(i, len(lines)):
        if lines[j]:
            values = lines[j].split(',')
            for value in values:
                if value.strip():
                    measurements.append(float(value.strip()))
    
    # Check for violations
    alerts = []
    for index, value in enumerate(measurements):
        if ucl is not None and value > ucl:
            alerts.append({"index": index, "value": value, "rule": "beyond_ucl"})
        elif lcl is not None and value < lcl:
            alerts.append({"index": index, "value": value, "rule": "beyond_lcl"})
    
    # Output JSON
    result = {"alerts": alerts}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    process_streaming_measurements()