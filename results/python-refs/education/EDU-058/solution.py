import json
import sys

def main():
    # Read JSON input from stdin
    input_data = json.load(sys.stdin)
    
    meeting_duration_min = input_data["meeting_duration_min"]
    teachers = input_data["teachers"]
    
    for teacher in teachers:
        name = teacher["name"]
        available_slots = teacher["available_slots"]
        
        print(f"{name}:")
        
        for slot in available_slots:
            # Parse the start time
            hour, minute = map(int, slot.split(':'))
            
            # Calculate end time
            end_minute = minute + meeting_duration_min
            end_hour = hour
            
            # Handle minute overflow
            if end_minute >= 60:
                end_hour += end_minute // 60
                end_minute = end_minute % 60
            
            # Format the time slot
            start_time = f"{hour:02d}:{minute:02d}"
            end_time = f"{end_hour:02d}:{end_minute:02d}"
            
            print(f"  {start_time}-{end_time}")

if __name__ == "__main__":
    main()