import json
import sys

def generate_awards(students):
    results = []
    
    for student_data in students:
        student = student_data["student"]
        gpa = student_data["gpa"]
        attendance_pct = student_data["attendance_pct"]
        participation_score = student_data["participation_score"]
        
        awards = []
        
        # Academic Excellence: GPA >= 3.8
        if gpa >= 3.8:
            awards.append("Academic Excellence")
        
        # Perfect Attendance: attendance >= 95%
        if attendance_pct >= 95:
            awards.append("Perfect Attendance")
        
        # Most Engaged: participation score >= 8
        if participation_score >= 8:
            awards.append("Most Engaged")
        
        if awards:
            results.append(f"{student}: {', '.join(awards)}")
    
    return results

# Read input from stdin
input_data = sys.stdin.read().strip()
students = json.loads(input_data)

# Generate awards
award_results = generate_awards(students)

# Output results
for result in award_results:
    print(result)