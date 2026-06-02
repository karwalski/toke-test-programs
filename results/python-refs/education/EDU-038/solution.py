import sys

# Read input from stdin
grades_input = input().strip()
grades = grades_input.split()

# Count occurrences of each grade
grade_counts = {}
for grade in grades:
    grade_counts[grade] = grade_counts.get(grade, 0) + 1

# Define the order of grades
grade_order = ['A', 'B', 'C', 'D', 'F']

# Output histogram
for grade in grade_order:
    if grade in grade_counts:
        count = grade_counts[grade]
        bars = '#' * count
        print(f"{grade}: {bars} ({count})")