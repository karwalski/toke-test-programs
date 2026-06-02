import json
import sys

data = json.load(sys.stdin)

for student_data in data:
    student = student_data["student"]
    grades = student_data["grades"]
    
    strongest_subject = max(grades, key=grades.get)
    strongest_score = grades[strongest_subject]
    
    weakest_subject = min(grades, key=grades.get)
    weakest_score = grades[weakest_subject]
    
    print(f"{student}: strongest={strongest_subject} ({strongest_score}), weakest={weakest_subject} ({weakest_score})")