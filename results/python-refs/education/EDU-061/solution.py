import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse JSON
students = json.loads(input_data)

# Dictionary to store subject totals and counts
subject_data = {}

# Process each student
for student in students:
    grades = student["grades"]
    for subject, score in grades.items():
        if subject not in subject_data:
            subject_data[subject] = {"total": 0, "count": 0}
        subject_data[subject]["total"] += score
        subject_data[subject]["count"] += 1

# Calculate averages and sort by subject name
results = []
for subject in sorted(subject_data.keys()):
    average = subject_data[subject]["total"] / subject_data[subject]["count"]
    results.append(f"{subject}: {average}")

# Output results
for result in results:
    print(result)