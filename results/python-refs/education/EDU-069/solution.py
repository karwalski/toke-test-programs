import json
import sys

def score_to_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

input_data = sys.stdin.read().strip()
records = json.loads(input_data)

for record in records:
    student = record['student']
    course = record['course']
    completion_date = record['completion_date']
    score = record['score']
    grade = score_to_grade(score)
    
    print(f"CERTIFICATE | {student} | {course} | {completion_date} | {grade}")