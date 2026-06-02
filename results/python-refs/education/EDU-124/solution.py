import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

class_name = input_data["class_name"]
students = input_data["students"]

# Get all unique assignments
assignments = set()
for student in students:
    assignments.update(student["grades"].keys())
assignments = sorted(assignments)

# Print header
print(f"Grade Book: {class_name}")

# Calculate column widths
name_width = max(len("Name"), max(len(student["name"]) for student in students))
assignment_widths = {}
for assignment in assignments:
    assignment_widths[assignment] = max(len(assignment), max(len(str(student["grades"].get(assignment, ""))) for student in students))
avg_width = len("Avg")

# Print column headers
header = "Name".ljust(name_width) + " |"
for assignment in assignments:
    header += f" {assignment.ljust(assignment_widths[assignment])} |"
header += " Avg"
print(header)

# Print each student's row
for student in students:
    name = student["name"]
    grades = student["grades"]
    
    # Calculate average
    grade_values = [grades.get(assignment, 0) for assignment in assignments if assignment in grades]
    avg = sum(grade_values) / len(grade_values) if grade_values else 0
    
    # Build row
    row = name.ljust(name_width) + " |"
    for assignment in assignments:
        score = grades.get(assignment, "")
        row += f" {str(score).ljust(assignment_widths[assignment])} |"
    row += f" {avg}"
    print(row)