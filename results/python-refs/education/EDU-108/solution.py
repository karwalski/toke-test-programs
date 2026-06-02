import json
import sys

def get_mastery_level(score):
    if score >= 80:
        return "M"
    elif score >= 60:
        return "D"
    else:
        return "N"

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

standards = input_data["standards"]
student_scores = input_data["student_scores"]

# Create a dictionary to store student scores by standard
student_data = {}
for score_entry in student_scores:
    student = score_entry["student"]
    standard_id = score_entry["standard_id"]
    score = score_entry["score"]
    
    if student not in student_data:
        student_data[student] = {}
    
    student_data[student][standard_id] = get_mastery_level(score)

# Print header
header = "Student"
for standard in standards:
    header += " | " + standard
print(header)

# Print each student's row
for student in sorted(student_data.keys()):
    row = student
    for standard in standards:
        mastery = student_data[student].get(standard, "N")
        row += " | " + mastery
    print(row)