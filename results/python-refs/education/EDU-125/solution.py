import json
import sys

# Read JSON input from stdin
input_data = json.loads(sys.stdin.read())

# Extract values from JSON
student_name = input_data["student_name"]
course_name = input_data["course_name"]
institution_name = input_data["institution_name"]
date = input_data["date"]

# Generate the pledge document
pledge = f"""ACADEMIC INTEGRITY PLEDGE
{institution_name}

I, {student_name}, enrolled in {course_name}, hereby pledge to uphold academic integrity in all my work.

I will not plagiarise, cheat, or misrepresent my work.
I will cite all sources properly.
I understand the consequences of academic dishonesty.

Signed: {student_name}
Date: {date}"""

# Output the pledge
print(pledge)