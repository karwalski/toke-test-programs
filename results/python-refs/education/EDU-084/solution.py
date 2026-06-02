import json
import sys
from datetime import datetime, timedelta

def generate_academic_calendar():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Parse dates
    semester_start = datetime.strptime(input_data["semester_start"], "%Y-%m-%d")
    semester_end = datetime.strptime(input_data["semester_end"], "%Y-%m-%d")
    events = input_data["events"]
    
    # Create event dictionary for quick lookup
    event_dict = {}
    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")
        event_dict[event_date] = event["name"]
    
    # Generate calendar weeks
    current_date = semester_start
    week_number = 1
    
    while current_date <= semester_end:
        # Calculate week end (Sunday to Saturday week, but starting from semester start day)
        week_end = current_date + timedelta(days=6)
        if week_end > semester_end:
            week_end = semester_end
        
        # Print week header
        print(f"Week {week_number}: {current_date.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}")
        
        # Check for events in this week
        check_date = current_date
        while check_date <= week_end:
            if check_date in event_dict:
                print(f"  {check_date.strftime('%Y-%m-%d')}: {event_dict[check_date]}")
            check_date += timedelta(days=1)
        
        # Move to next week
        current_date += timedelta(days=7)
        week_number += 1

generate_academic_calendar()