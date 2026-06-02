import csv
import json
import sys
import statistics

def determine_sampling_rate(defect_rates):
    current_rate = statistics.mean(defect_rates)
    
    # Calculate variation in defect rates
    if len(defect_rates) > 1:
        stdev = statistics.stdev(defect_rates)
        variation = stdev / current_rate if current_rate > 0 else 0
    else:
        variation = 0
    
    # Determine sampling strategy based on current rate and variation
    if current_rate <= 0.015 and variation <= 0.5:
        # Low defect rate and stable process
        recommended_sampling = "reduced"
        sample_pct = 5
        reason = "stable_process"
    elif current_rate > 0.05 or variation > 1.0:
        # High defect rate or unstable process
        recommended_sampling = "increased"
        sample_pct = 20
        reason = "high_defect_rate" if current_rate > 0.05 else "unstable_process"
    else:
        # Moderate defect rate
        recommended_sampling = "standard"
        sample_pct = 10
        reason = "moderate_defect_rate"
    
    return {
        "current_rate": current_rate,
        "recommended_sampling": recommended_sampling,
        "sample_pct": sample_pct,
        "reason": reason
    }

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
defect_rates = []

for row in reader:
    defect_rates.append(float(row['defect_rate']))

# Determine optimal sampling rate
result = determine_sampling_rate(defect_rates)

# Output JSON to stdout
print(json.dumps(result, separators=(',', ':')))