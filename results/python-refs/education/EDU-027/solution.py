import json
from datetime import datetime

# Read input
reference_date = input().strip()
days_window = int(input().strip())
assignments_json = input().strip()

# Parse the reference date
ref_date = datetime.strptime(reference_date, "%Y-%m-%d")

# Parse the assignments JSON
assignments = json.loads(assignments_json)

# Find assignments due within the window
upcoming = []
for assignment in assignments:
    due_date = datetime.strptime(assignment["due_date"], "%Y-%m-%d")
    days_diff = (due_date - ref_date).days
    
    # Check if assignment is due within the window (0 to days_window inclusive)
    if 0 <= days_diff <= days_window:
        upcoming.append((days_diff, assignment["title"], due_date))

# Sort by due date
upcoming.sort(key=lambda x: x[2])

# Output results
if upcoming:
    for days_left, title, _ in upcoming:
        print(f"{days_left} days left: {title}")
else:
    print("No upcoming deadlines")