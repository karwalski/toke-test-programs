import csv
import json
import sys

def main():
    reader = csv.DictReader(sys.stdin)
    
    batches = []
    all_values = []
    
    for row in reader:
        batch_name = row['batch']
        values_str = row['values']
        
        # Parse semicolon-separated values
        values = [float(x) for x in values_str.split(';')]
        
        # Calculate mean for this batch
        batch_mean = sum(values) / len(values)
        
        batches.append({
            "batch": batch_name,
            "mean": round(batch_mean, 1)
        })
        
        # Add to all values for aggregate calculation
        all_values.extend(values)
    
    # Calculate aggregate mean
    aggregate_mean = sum(all_values) / len(all_values)
    
    result = {
        "batches": batches,
        "aggregate_mean": round(aggregate_mean, 1)
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()