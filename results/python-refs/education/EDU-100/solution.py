import json
import sys

# Read input from stdin
input_data = sys.stdin.read().strip()
students = json.loads(input_data)

# Sort students by score in descending order, then by name for consistent ordering
students.sort(key=lambda x: (-x["score"], x["student"]))

# Calculate rankings with dense ranking (ties share same rank, next rank is consecutive)
current_rank = 1
previous_score = None

for student in students:
    if previous_score is not None and student["score"] < previous_score:
        current_rank += 1
    
    print(f"{current_rank}. {student['student']} - {student['score']}")
    previous_score = student["score"]