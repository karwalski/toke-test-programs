import sys
import re

# Read input
lines = sys.stdin.read().strip().split('\n')
flagged_words = [word.strip() for word in lines[0].split(',')]
text_lines = lines[1:]

matches = []

# Process each text line
for line_num, line in enumerate(text_lines, 1):
    for word in flagged_words:
        # Find all occurrences of the word (case-sensitive, whole words)
        pattern = r'\b' + re.escape(word) + r'\b'
        for match in re.finditer(pattern, line):
            col = match.start() + 1  # 1-based column numbering
            matches.append((line_num, col, word))

# Sort matches by line number, then by column
matches.sort(key=lambda x: (x[0], x[1]))

# Output results
if matches:
    for line_num, col, word in matches:
        print(f"Line {line_num}, col {col}: {word}")
else:
    print("CLEAN")