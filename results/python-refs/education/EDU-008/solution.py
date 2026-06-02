import sys

# Grade to GPA mapping
grade_points = {
    'A': 4.0,
    'B': 3.0,
    'C': 2.0,
    'D': 1.0,
    'F': 0.0
}

total_quality_points = 0.0
total_credits = 0

# Read input and process each course
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split()
    course_name = parts[0]
    credits = int(parts[1])
    grade = parts[2]
    
    # Calculate quality points for this course
    quality_points = credits * grade_points[grade]
    total_quality_points += quality_points
    total_credits += credits
    
    # Print course quality points
    print(f"{course_name}: {quality_points} quality points")

# Calculate and print GPA
gpa = total_quality_points / total_credits
print(f"GPA: {gpa:.2f}")