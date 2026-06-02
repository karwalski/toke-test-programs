import json
import sys

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

total_students = input_data["total_students"]
engagement_events = input_data["engagement_events"]

# Count events per student
student_counts = {}
for event in engagement_events:
    student = event["student"]
    if student in student_counts:
        student_counts[student] += 1
    else:
        student_counts[student] = 1

# Generate all student names (A, B, C, etc.)
all_students = []
for i in range(total_students):
    all_students.append(chr(ord('A') + i))

# Output per-student engagement scores
for student in all_students:
    count = student_counts.get(student, 0)
    print(f"{student}: {count} events")

# Calculate engagement rate
engaged_students = len([s for s in all_students if student_counts.get(s, 0) > 0])
engagement_rate = round((engaged_students / total_students) * 100)
print(f"Engagement rate: {engagement_rate}%")