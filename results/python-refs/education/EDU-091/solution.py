import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
events = json.loads(input_data)

# Point values for each event type
point_values = {
    "question": 2,
    "answer": 1,
    "comment": 1
}

# Track points for each student
student_points = {}

# Calculate points for each event
for event in events:
    student = event["student"]
    event_type = event["event_type"]
    points = point_values.get(event_type, 0)
    
    if student not in student_points:
        student_points[student] = 0
    student_points[student] += points

# Sort by points descending, then by student name for ties
sorted_students = sorted(student_points.items(), key=lambda x: (-x[1], x[0]))

# Output results
for student, points in sorted_students:
    print(f"{student}: {points} points")