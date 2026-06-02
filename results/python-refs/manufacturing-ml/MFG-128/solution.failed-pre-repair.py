import sys
import csv
import json

def calculate_kaplan_meier():
    # Read CSV from stdin
    reader = csv.DictReader(sys.stdin)
    data = []
    for row in reader:
        time = int(row['time'])
        event = int(row['event'])
        data.append((time, event))
    
    # Sort by time
    data.sort(key=lambda x: x[0])
    
    # Calculate Kaplan-Meier survival curve
    survival_curve = [{"time": 0, "survival": 1.0}]
    
    n_at_risk = len(data)
    survival_prob = 1.0
    
    i = 0
    while i < len(data):
        current_time = data[i][0]
        
        # Count events and censored at this time point
        events = 0
        censored = 0
        j = i
        
        while j < len(data) and data[j][0] == current_time:
            if data[j][1] == 1:  # failure
                events += 1
            else:  # censored
                censored += 1
            j += 1
        
        # Update survival probability only if there are events
        if events > 0:
            survival_prob *= (n_at_risk - events) / n_at_risk
            survival_curve.append({"time": current_time, "survival": survival_prob})
        
        # Update number at risk
        n_at_risk -= (events + censored)
        i = j
    
    # Calculate median survival
    median_survival = None
    for k in range(len(survival_curve) - 1):
        if survival_curve[k]["survival"] >= 0.5 and survival_curve[k + 1]["survival"] < 0.5:
            # Linear interpolation
            t1, s1 = survival_curve[k]["time"], survival_curve[k]["survival"]
            t2, s2 = survival_curve[k + 1]["time"], survival_curve[k + 1]["survival"]
            
            # Interpolate to find time where survival = 0.5
            median_survival = t1 + (0.5 - s1) * (t2 - t1) / (s2 - s1)
            median_survival = int(median_survival)
            break
    
    result = {
        "survival_curve": survival_curve,
        "median_survival": median_survival
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    calculate_kaplan_meier()