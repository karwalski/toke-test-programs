import re
import sys

# Read the regex pattern from the first line
pattern = input().strip()

# Compile the regex pattern
try:
    regex = re.compile(pattern)
except re.error:
    # If pattern is invalid, treat all strings as non-matching
    regex = None

# Read all remaining lines (test strings)
test_strings = []
try:
    while True:
        line = input()
        test_strings.append(line)
except EOFError:
    pass

# Test each string and count matches
match_count = 0
total_count = len(test_strings)

for test_string in test_strings:
    if regex and regex.match(test_string):
        print(f"MATCH: {test_string}")
        match_count += 1
    else:
        print(f"NO MATCH: {test_string}")

# Print summary
print(f"{match_count}/{total_count} matched")