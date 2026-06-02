import json
import sys

def grade_to_points(grade):
    grade_map = {
        'A': 4.0,
        'B': 3.0,
        'C': 2.0,
        'D': 1.0,
        'F': 0.0
    }
    return grade_map.get(grade, 0.0)

def calculate_gpa(courses):
    total_points = 0
    total_credits = 0
    
    for course in courses:
        points = grade_to_points(course['grade'])
        credits = course['credits']
        total_points += points * credits
        total_credits += credits
    
    if total_credits == 0:
        return 0.0
    
    return total_points / total_credits

def get_standing(gpa):
    if gpa >= 3.5:
        return "Excellent"
    elif gpa >= 3.0:
        return "Good"
    elif gpa >= 2.0:
        return "Satisfactory"
    else:
        return "Poor"

def generate_report(student_data):
    name = student_data['name']
    student_id = student_data['id']
    courses = student_data['courses']
    
    # Header
    print("Student Report")
    print(f"Name: {name} | ID: {student_id}")
    print("---")
    
    # Course table
    for course in courses:
        course_name = course['name']
        credits = course['credits']
        grade = course['grade']
        print(f"{course_name:<7} {credits}cr  {grade}")
    
    print("---")
    
    # GPA and standing
    gpa = calculate_gpa(courses)
    standing = get_standing(gpa)
    print(f"GPA: {gpa:.2f} | Standing: {standing}")

# Read from stdin
input_data = sys.stdin.read().strip()
student_data = json.loads(input_data)

# Generate report
generate_report(student_data)