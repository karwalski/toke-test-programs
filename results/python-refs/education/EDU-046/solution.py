import json
import sys
from datetime import datetime

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

due_date = datetime.strptime(input_data["due_date"], "%Y-%m-%d")
total_students = input_data["total_students"]
submissions = input_data["submissions"]

on_time = 0
late = 0

# Count on-time and late submissions
for submission in submissions:
    submitted_date = datetime.strptime(submission["submitted_date"], "%Y-%m-%d")
    if submitted_date <= due_date:
        on_time += 1
    else:
        late += 1

# Calculate missing submissions
missing = total_students - len(submissions)

# Calculate percentages
on_time_pct = round(on_time * 100 / total_students)
late_pct = round(late * 100 / total_students)
missing_pct = round(missing * 100 / total_students)

# Output results
print(f"on_time: {on_time} ({on_time_pct}%)")
print(f"late: {late} ({late_pct}%)")
print(f"missing: {missing} ({missing_pct}%)")