import csv
import json
import sys
import statistics

def main():
    # Read CSV data from stdin
    reader = csv.DictReader(sys.stdin)
    data = []
    
    for row in reader:
        timestamp = int(row['timestamp'])
        kwh = float(row['kwh'])
        production_units = int(row['production_units'])
        efficiency = kwh / production_units if production_units > 0 else 0
        
        data.append({
            'timestamp': timestamp,
            'kwh': kwh,
            'production_units': production_units,
            'efficiency': efficiency
        })
    
    # Calculate baseline efficiency (median of all efficiency values)
    efficiencies = [d['efficiency'] for d in data]
    baseline = statistics.median(efficiencies)
    
    # Detect anomalies (efficiency significantly higher than baseline)
    # Using 1.5x baseline as threshold for anomaly detection
    anomalies = []
    threshold = baseline * 1.5
    
    for point in data:
        if point['efficiency'] > threshold:
            anomalies.append({
                'timestamp': point['timestamp'],
                'actual': round(point['efficiency'], 2),
                'expected': baseline
            })
    
    # Format output
    result = {
        'baseline_kwh_per_unit': baseline,
        'anomalies': anomalies
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == '__main__':
    main()