import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
students = json.loads(input_data)

# Dictionary to track top performer for each subject
top_performers = {}

# Process each student
for student_data in students:
    student_name = student_data["student"]
    grades = student_data["grades"]
    
    # Check each subject for this student
    for subject, score in grades.items():
        if subject not in top_performers or score > top_performers[subject][1]:
            top_performers[subject] = (student_name, score)

# Sort subjects alphabetically and output results
for subject in sorted(top_performers.keys()):
    student_name, score = top_performers[subject]
    print(f"{subject}: {student_name} ({score})")