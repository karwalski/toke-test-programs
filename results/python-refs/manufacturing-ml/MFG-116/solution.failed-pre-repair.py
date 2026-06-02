import csv
import json
import sys

def calculate_health_score(noise_level, drift_rate, dropout_pct):
    # Calculate health score based on the three metrics
    # Lower values are better, so we subtract from 100
    
    # Normalize and weight the metrics
    noise_penalty = noise_level * 1000  # Scale up noise impact
    drift_penalty = drift_rate * 1000   # Scale up drift impact
    dropout_penalty = dropout_pct       # Dropout is already in percentage
    
    # Calculate total penalty
    total_penalty = noise_penalty + drift_penalty + dropout_penalty
    
    # Health score is 100 minus total penalty, with a minimum of 0
    health_score = max(0, 100 - total_penalty)
    
    return int(round(health_score))

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
sensors = []

for row in reader:
    sensor_id = row['sensor_id']
    noise_level = float(row['noise_level'])
    drift_rate = float(row['drift_rate'])
    dropout_pct = float(row['dropout_pct'])
    
    health_score = calculate_health_score(noise_level, drift_rate, dropout_pct)
    
    sensors.append({
        'sensor_id': sensor_id,
        'health_score': health_score
    })

# Sort sensors by health score (lowest first) to determine priority
priority = sorted(sensors, key=lambda x: x['health_score'])
priority_list = [sensor['sensor_id'] for sensor in priority]

# Create output dictionary
output = {
    'sensors': sensors,
    'priority': priority_list
}

# Output JSON
print(json.dumps(output, separators=(',', ':')))