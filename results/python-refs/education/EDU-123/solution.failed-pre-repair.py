import json
import sys
from datetime import datetime, timedelta

def solve_assessment_scheduling():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    start_date_str = input_data["start_date"]
    excluded_dates = set(input_data["excluded_dates"])
    assessments = input_data["assessments"]
    
    # Parse start date
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    
    # Track assigned dates and results
    assigned_dates = set()
    results = []
    
    current_date = start_date
    
    for assessment in assessments:
        title = assessment["title"]
        min_days_gap = assessment["min_days_gap"]
        
        # Find the next available date
        candidate_date = current_date
        
        while True:
            candidate_date_str = candidate_date.strftime("%Y-%m-%d")
            
            # Check if date is excluded or already assigned
            if (candidate_date_str not in excluded_dates and 
                candidate_date_str not in assigned_dates):
                break
            
            candidate_date += timedelta(days=1)
        
        # Assign this date
        assigned_date_str = candidate_date.strftime("%Y-%m-%d")
        assigned_dates.add(assigned_date_str)
        results.append(f"{title}: {assigned_date_str}")
        
        # Update current_date for next assessment (considering min_days_gap)
        current_date = candidate_date + timedelta(days=min_days_gap)
    
    # Output results
    for result in results:
        print(result)

if __name__ == "__main__":
    solve_assessment_scheduling()