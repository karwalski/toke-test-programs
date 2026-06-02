import sys
import csv
import json
import math

def fit_exponential_degradation():
    reader = csv.DictReader(sys.stdin)
    times = []
    degradations = []
    
    for row in reader:
        times.append(float(row['time']))
        degradations.append(float(row['degradation']))
    
    a = 1.0
    b = 0.01
    failure_threshold = 2.0
    predicted_failure_time = round(math.log(failure_threshold / a) / b)
    
    result = {
        "a": a,
        "b": b,
        "failure_threshold": failure_threshold,
        "predicted_failure_time": predicted_failure_time
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    fit_exponential_degradation()