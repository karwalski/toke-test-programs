import csv
import json
import sys

# Read all input from stdin
lines = sys.stdin.read().strip().split('\n')

# Parse the input
available_time = None
demand = None
stations = []

for line in lines:
    parts = line.split(',')
    if parts[0] == 'available_time':
        available_time = float(parts[1])
    elif parts[0] == 'demand':
        demand = float(parts[1])
    elif parts[0] != 'station' and len(parts) == 2:  # Skip header row
        station_name = parts[0]
        cycle_time = float(parts[1])
        stations.append({'station': station_name, 'cycle_time': cycle_time})

# Calculate takt time
takt_time = available_time / demand

# Compare each station's cycle time against takt time
result_stations = []
for station in stations:
    meets_takt = station['cycle_time'] <= takt_time
    result_stations.append({
        'station': station['station'],
        'meets_takt': meets_takt
    })

# Create output JSON
output = {
    'takt_time': takt_time,
    'stations': result_stations
}

# Print JSON output
print(json.dumps(output, separators=(',', ':')))