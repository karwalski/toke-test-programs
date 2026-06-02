import csv
import json
import sys
from statistics import mean

def detect_drift():
    # Read CSV from stdin
    reader = csv.DictReader(sys.stdin)
    readings = []
    
    for row in reader:
        timestamp = float(row['timestamp'])
        reading = float(row['reading'])
        readings.append((timestamp, reading))
    
    if len(readings) < 2:
        result = {"drift_detected": False, "drift_rate": 0.0, "direction": "none"}
        print(json.dumps(result, separators=(',', ':')))
        return
    
    # Calculate differences between consecutive readings
    diffs = []
    for i in range(1, len(readings)):
        time_diff = readings[i][0] - readings[i-1][0]
        reading_diff = readings[i][1] - readings[i-1][1]
        if time_diff > 0:
            rate = reading_diff / time_diff
            diffs.append(rate)
    
    if not diffs:
        result = {"drift_detected": False, "drift_rate": 0.0, "direction": "none"}
        print(json.dumps(result, separators=(',', ':')))
        return
    
    # Calculate average drift rate
    avg_drift_rate = mean(diffs)
    
    # Determine if drift is detected (non-zero rate)
    drift_detected = abs(avg_drift_rate) > 1e-10
    
    # Determine direction
    if avg_drift_rate > 1e-10:
        direction = "increasing"
    elif avg_drift_rate < -1e-10:
        direction = "decreasing"
    else:
        direction = "stable"
        drift_detected = False
    
    result = {
        "drift_detected": drift_detected,
        "drift_rate": round(avg_drift_rate, 10),
        "direction": direction
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    detect_drift()