import sys

# Read all input
lines = sys.stdin.read().splitlines()

# First line is the target style
target_style = lines[0]

# Process remaining lines
for i in range(1, len(lines)):
    line = lines[i].strip()
    
    # Check if line is a horizontal rule (3 or more of the same character)
    if len(line) >= 3:
        # Check for --- style
        if all(c == '-' for c in line):
            print(target_style)
        # Check for *** style  
        elif all(c == '*' for c in line):
            print(target_style)
        # Check for ___ style
        elif all(c == '_' for c in line):
            print(target_style)
        else:
            print(lines[i])
    else:
        print(lines[i])