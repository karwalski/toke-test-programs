import sys

text = sys.stdin.read()

# Replace all whitespace except newlines with single spaces
# Split by newlines to preserve them
lines = text.split('\n')

normalized_lines = []
for line in lines:
    # Replace all whitespace in the line with spaces, then normalize multiple spaces
    normalized_line = ''
    prev_was_space = False
    
    for char in line:
        if char.isspace():  # This includes tabs, spaces, etc. but not newlines since we split on them
            if not prev_was_space:
                normalized_line += ' '
            prev_was_space = True
        else:
            normalized_line += char
            prev_was_space = False
    
    normalized_lines.append(normalized_line)

# Join back with newlines
result = '\n'.join(normalized_lines)
print(result, end='')