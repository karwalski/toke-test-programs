import json
import sys

# Read JSON input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract data from JSON
student_name = input_data["student_name"]
assignment = input_data["assignment"]
score = input_data["score"]
max_score = input_data["max_score"]
strengths = input_data["strengths"]
improvements = input_data["improvements"]

# Calculate percentage
percentage = int(score * 100 / max_score)

# Generate feedback
print(f"Feedback for {student_name} - {assignment}")
print(f"Score: {score}/{max_score} ({percentage}%)")
print()
print("Strengths:")
for strength in strengths:
    print(f"- {strength}")
print()
print("Areas for Improvement:")
for improvement in improvements:
    print(f"- {improvement}")
print()
print("Keep up the good work!")