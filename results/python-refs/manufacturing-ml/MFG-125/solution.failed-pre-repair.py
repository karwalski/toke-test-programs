import sys
import json
import csv
from io import StringIO

def main():
    input_data = sys.stdin.read().strip()
    lines = input_data.split('\n')
    
    # Find where spec_data starts
    spec_data_idx = lines.index('spec_data')
    
    # Parse zone specifications
    zones = {}
    for i in range(1, spec_data_idx):
        if lines[i].strip():
            parts = lines[i].split(',')
            zone_name = parts[0]
            zones[zone_name] = {
                'min_time': int(parts[1]),
                'max_time': int(parts[2]),
                'min_temp': int(parts[3]),
                'max_temp': int(parts[4])
            }
    
    # Parse temperature data
    temp_data = []
    for i in range(spec_data_idx + 2, len(lines)):
        if lines[i].strip():
            time_val, temp_val = lines[i].split(',')
            temp_data.append((int(time_val), int(temp_val)))
    
    # Calculate metrics
    peak_temp = max(temp for _, temp in temp_data)
    
    # Calculate time above 230°C (reflow temperature)
    time_above_230 = 0
    for i in range(len(temp_data) - 1):
        t1, temp1 = temp_data[i]
        t2, temp2 = temp_data[i + 1]
        
        # If both points are above 230, add the full interval
        if temp1 >= 230 and temp2 >= 230:
            time_above_230 += (t2 - t1)
        # If one point crosses 230, calculate partial time
        elif temp1 >= 230 or temp2 >= 230:
            if temp1 < 230:
                # Interpolate when it crosses 230
                cross_time = t1 + (230 - temp1) * (t2 - t1) / (temp2 - temp1)
                time_above_230 += (t2 - cross_time)
            else:
                # temp2 < 230
                cross_time = t1 + (230 - temp1) * (t2 - t1) / (temp2 - temp1)
                time_above_230 += (cross_time - t1)
    
    # Calculate cooling rate (from peak to end)
    peak_idx = 0
    for i, (_, temp) in enumerate(temp_data):
        if temp == peak_temp:
            peak_idx = i
            break
    
    # Find cooling phase (after peak)
    cooling_start_time = temp_data[peak_idx][0]
    cooling_start_temp = temp_data[peak_idx][1]
    end_time = temp_data[-1][0]
    end_temp = temp_data[-1][1]
    
    cooling_rate = (cooling_start_temp - end_temp) / (end_time - cooling_start_time)
    
    # Check compliance (simplified - assume compliant if peak temp is within reflow zone)
    compliant = True
    reflow_zone = zones.get('reflow', {})
    if reflow_zone:
        if peak_temp < reflow_zone['min_temp'] or peak_temp > reflow_zone['max_temp']:
            compliant = False
    
    # Output JSON with exact formatting
    result = {
        "peak_temp": peak_temp,
        "time_above_230": int(time_above_230),
        "cooling_rate": round(cooling_rate, 1),
        "compliant": compliant
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()