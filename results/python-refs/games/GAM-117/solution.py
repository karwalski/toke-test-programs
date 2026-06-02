import sys

# Read all input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Find the blank line that separates taboo words from description
blank_line_index = -1
for i, line in enumerate(lines):
    if line == '':
        blank_line_index = i
        break

# Extract parts
target_word = lines[0]
taboo_words = lines[1:blank_line_index]
description = lines[blank_line_index + 1]

# Convert description to lowercase and split into words
description_words = description.lower().split()

# Check for taboo words
violations = []
for taboo in taboo_words:
    if taboo.lower() in description_words:
        violations.append(taboo.upper())

# Output result
if not violations:
    print("Pass")
else:
    for violation in violations:
        print(f"Taboo: {violation}")