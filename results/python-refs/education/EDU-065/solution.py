import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
records = json.loads(input_data)

# Dictionary to store student totals
student_totals = {}

# Process each record
for record in records:
    student = record["student"]
    points_earned = record["points_earned"]
    points_possible = record["points_possible"]
    
    if student not in student_totals:
        student_totals[student] = {"earned": 0, "possible": 0}
    
    student_totals[student]["earned"] += points_earned
    student_totals[student]["possible"] += points_possible

# Calculate percentages and create output list
results = []
for student, totals in student_totals.items():
    earned = totals["earned"]
    possible = totals["possible"]
    percentage = round(earned / possible * 100) if possible > 0 else 0
    results.append((student, earned, possible, percentage))

# Sort by percentage descending
results.sort(key=lambda x: x[3], reverse=True)

# Output results
for student, earned, possible, percentage in results:
    print(f"{student}: {earned}/{possible} ({percentage}%)")