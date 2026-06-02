import csv
import json
import sys

def calculate_health_score(noise_level, drift_rate, dropout_pct):
    # Normalize each metric to 0-100 penalty scale
    # S1: noise=0.01, drift=0.001, dropout=0.1 -> 98
    # S2: noise=0.05, drift=0.01, dropout=2.0 -> 85
    # S3: noise=0.1, drift=0.02, dropout=5.0 -> 65
    
    # Normalize: noise max ~0.1, drift max ~0.02, dropout max ~5-10
    noise_norm = min(noise_level / 0.1, 1.0) * 100
    drift_norm = min(drift_rate / 0.02, 1.0) * 100
    dropout_norm = min(dropout_pct / 10.0, 1.0) * 100
    
    penalty = 0.3 * noise_norm + 0.4 * drift_norm + 0.3 * dropout_norm
    health_score = max(0, 100 - penalty)
    
    return int(round(health_score))

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

priority = sorted(sensors, key=lambda x: x['health_score'])
priority_list = [sensor['sensor_id'] for sensor in priority]

output = {
    'sensors': sensors,
    'priority': priority_list
}

print(json.dumps(output, separators=(',', ':')))