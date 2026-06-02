import sys

total_weighted_score = 0.0

for line in sys.stdin:
    line = line.strip()
    if line:
        parts = line.split()
        component = parts[0]
        weight = float(parts[1])
        score = float(parts[2])
        total_weighted_score += weight * score

# Determine letter grade
if total_weighted_score >= 90:
    letter_grade = 'A'
elif total_weighted_score >= 80:
    letter_grade = 'B'
elif total_weighted_score >= 70:
    letter_grade = 'C'
elif total_weighted_score >= 60:
    letter_grade = 'D'
else:
    letter_grade = 'F'

print(f"weighted_total: {total_weighted_score}")
print(f"letter_grade: {letter_grade}")