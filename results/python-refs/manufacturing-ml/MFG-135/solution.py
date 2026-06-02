import sys
import csv
import json

def calculate_deviations():
    # Read CSV from stdin
    csv_reader = csv.DictReader(sys.stdin)
    
    deviations = []
    alerts = []
    
    for row in csv_reader:
        parameter = row['parameter']
        predicted = float(row['predicted'])
        actual = float(row['actual'])
        tolerance = float(row['tolerance'])
        
        # Calculate absolute deviation
        deviation = abs(actual - predicted)
        
        # Calculate score (deviation / tolerance)
        score = deviation / tolerance
        
        # Add to deviations list
        deviations.append({
            "parameter": parameter,
            "deviation": deviation,
            "score": score
        })
        
        # Check if deviation exceeds tolerance (score >= 1.0)
        if score >= 1.0:
            alerts.append(parameter)
    
    # Calculate overall health (average of all scores)
    overall_health = sum(d['score'] for d in deviations) / len(deviations)
    
    # Create output JSON
    result = {
        "deviations": deviations,
        "overall_health": overall_health,
        "alerts": alerts
    }
    
    # Print JSON without spaces after separators to match expected output
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    calculate_deviations()