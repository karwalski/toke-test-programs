import sys

for line in sys.stdin:
    score = int(line.strip())
    
    if score >= 130:
        classification = "Very Superior"
    elif score >= 120:
        classification = "Superior"
    elif score >= 110:
        classification = "High Average"
    elif score >= 90:
        classification = "Average"
    elif score >= 80:
        classification = "Low Average"
    elif score >= 70:
        classification = "Borderline"
    else:
        classification = "Extremely Low"
    
    print(f"{score}: {classification}")