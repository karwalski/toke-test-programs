import sys
import csv
from io import StringIO

def main():
    # Read all input
    input_lines = []
    for line in sys.stdin:
        input_lines.append(line.rstrip('\n'))
    
    # Find the blank line that separates funnel steps from CSV data
    blank_line_idx = input_lines.index('')
    
    # Extract funnel steps
    funnel_steps = input_lines[:blank_line_idx]
    
    # Extract CSV data
    csv_lines = input_lines[blank_line_idx + 1:]
    csv_data = '\n'.join(csv_lines)
    
    # Parse CSV data
    csv_reader = csv.DictReader(StringIO(csv_data))
    events = list(csv_reader)
    
    # Group events by user
    user_events = {}
    for event in events:
        user_id = event['user_id']
        event_name = event['event']
        if user_id not in user_events:
            user_events[user_id] = []
        user_events[user_id].append(event_name)
    
    # Calculate funnel metrics
    step_users = []
    
    for i, step in enumerate(funnel_steps):
        users_at_step = set()
        
        for user_id, events_list in user_events.items():
            # Check if user reached this step
            if step in events_list:
                # For first step, just check if they have the event
                if i == 0:
                    users_at_step.add(user_id)
                else:
                    # For subsequent steps, check if they completed all previous steps
                    completed_all_previous = True
                    for prev_step in funnel_steps[:i]:
                        if prev_step not in events_list:
                            completed_all_previous = False
                            break
                    if completed_all_previous:
                        users_at_step.add(user_id)
        
        step_users.append(len(users_at_step))
    
    # Output results
    for i, step in enumerate(funnel_steps):
        users = step_users[i]
        
        if i == 0:
            # First step
            conversion_from_top = 100.00
            print(f"{step}: {users} users ({conversion_from_top:.2f}% from top)")
        else:
            # Subsequent steps
            conversion_from_prev = (users / step_users[i-1]) * 100 if step_users[i-1] > 0 else 0
            conversion_from_top = (users / step_users[0]) * 100 if step_users[0] > 0 else 0
            print(f"{step}: {users} users ({conversion_from_prev:.2f}% from prev, {conversion_from_top:.2f}% from top)")

if __name__ == "__main__":
    main()