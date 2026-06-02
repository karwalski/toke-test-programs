import sys
import csv
import json
import statistics

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
data = {}

for row in reader:
    station = row['station']
    cycle_time = float(row['cycle_time'])
    
    if station not in data:
        data[station] = []
    data[station].append(cycle_time)

# Calculate statistics for each station
stations = []
max_mean = 0
bottleneck = ""

for station in sorted(data.keys()):
    cycle_times = data[station]
    mean_val = statistics.mean(cycle_times)
    std_val = statistics.stdev(cycle_times) if len(cycle_times) > 1 else 0.0
    
    stations.append({
        "station": station,
        "mean": mean_val,
        "std": std_val
    })
    
    # Track bottleneck (station with highest mean)
    if mean_val > max_mean:
        max_mean = mean_val
        bottleneck = station

# Create output
result = {
    "stations": stations,
    "bottleneck": bottleneck
}

print(json.dumps(result, separators=(',', ':')))