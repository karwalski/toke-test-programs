import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Calculate hotspot scores and determine risk levels
results = []
for item in input_data:
    file = item["file"]
    complexity = item["complexity"]
    churn_count = item["churn_count"]
    
    # Calculate hotspot score as complexity * churn_count
    score = complexity * churn_count
    
    # Determine risk level based on score
    if score >= 100:
        risk_level = "HIGH RISK"
    elif score >= 10:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"
    
    results.append((file, score, risk_level))

# Sort by score descending
results.sort(key=lambda x: x[1], reverse=True)

# Output results
for file, score, risk_level in results:
    print(f"{file}: score={score} [{risk_level}]")