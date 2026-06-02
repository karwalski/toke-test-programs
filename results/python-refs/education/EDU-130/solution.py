import json
import sys

def calculate_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    else:
        return 'F'

def calculate_gpa(grades):
    grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    total_points = sum(grade_points[grade] for grade in grades)
    return total_points / len(grades) if grades else 0.0

def generate_recommendation(gpa, attendance_rate):
    if gpa >= 2.0 and attendance_rate >= 0.8:
        return "Promote to next year"
    else:
        return "Retain for additional support"

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Extract data
name = input_data["name"]
year = input_data["year"]
semester_grades = input_data["semester_grades"]
attendance = input_data["attendance"]
teacher_comment = input_data["teacher_comment"]

# Calculate attendance rate
attendance_rate = attendance["present"] / attendance["total"]
attendance_percentage = round(attendance_rate * 100)

# Process grades
grades = []
total_gpa_points = 0

print(f"ANNUAL PROGRESS REPORT {year}")
print(f"Student: {name}")
print()
print("Academic Performance:")

for subject_data in semester_grades:
    subject = subject_data["subject"]
    s1 = subject_data["s1"]
    s2 = subject_data["s2"]
    avg = (s1 + s2) / 2
    grade = calculate_grade(avg)
    grades.append(grade)
    
    print(f"{subject}:    S1={s1}  S2={s2}  Avg={avg}  Grade={grade}")

print()
gpa = calculate_gpa(grades)
print(f"Overall GPA: {gpa:.2f}")
print()
print(f"Attendance: {attendance['present']}/{attendance['total']} ({attendance_percentage}%)")
print()
print("Teacher Comment:")
print(teacher_comment)
print()
recommendation = generate_recommendation(gpa, attendance_rate)
print(f"Recommendation: {recommendation}")