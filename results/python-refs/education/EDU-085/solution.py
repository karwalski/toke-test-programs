import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
students = json.loads(input_data)

# Calculate average difficulty for each subject
subject_totals = {}
subject_counts = {}

for student_data in students:
    subject_scores = student_data["subject_scores"]
    for subject, score in subject_scores.items():
        if subject not in subject_totals:
            subject_totals[subject] = 0
            subject_counts[subject] = 0
        subject_totals[subject] += score
        subject_counts[subject] += 1

# Calculate averages and sort by difficulty descending
subject_averages = []
for subject in subject_totals:
    avg = subject_totals[subject] / subject_counts[subject]
    subject_averages.append((subject, avg))

# Sort by average difficulty descending
subject_averages.sort(key=lambda x: x[1], reverse=True)

# Output results
for rank, (subject, avg) in enumerate(subject_averages, 1):
    print(f"{rank}. {subject}: {avg}")