import json
import sys
from datetime import datetime, timedelta

def solve_assessment_scheduling():
    input_data = json.loads(sys.stdin.read().strip())
    
    start_date_str = input_data["start_date"]
    excluded_dates = set(input_data["excluded_dates"])
    assessments = input_data["assessments"]
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    
    assigned_dates = set()
    results = []
    
    current_date = start_date
    last_assigned = None
    
    for i, assessment in enumerate(assessments):
        title = assessment["title"]
        min_days_gap = assessment["min_days_gap"]
        
        if last_assigned is None:
            candidate_date = current_date
        else:
            candidate_date = last_assigned + timedelta(days=max(1, min_days_gap))
        
        while True:
            candidate_date_str = candidate_date.strftime("%Y-%m-%d")
            if (candidate_date_str not in excluded_dates and 
                candidate_date_str not in assigned_dates):
                break
            candidate_date += timedelta(days=1)
        
        assigned_date_str = candidate_date.strftime("%Y-%m-%d")
        assigned_dates.add(assigned_date_str)
        results.append(f"{title}: {assigned_date_str}")
        last_assigned = candidate_date
    
    for result in results:
        print(result)

if __name__ == "__main__":
    solve_assessment_scheduling()