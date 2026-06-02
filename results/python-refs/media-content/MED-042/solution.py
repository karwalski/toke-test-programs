import sys
import re

for line in sys.stdin:
    line = line.strip()
    if line:
        # Insert underscore before uppercase letters that follow lowercase letters
        snake_case = re.sub(r'([a-z])([A-Z])', r'\1_\2', line)
        # Convert to lowercase
        snake_case = snake_case.lower()
        print(snake_case)