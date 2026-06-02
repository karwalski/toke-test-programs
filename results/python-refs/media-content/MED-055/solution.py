import sys

# Read the first line to get alignment and width
first_line = input().strip().split()
alignment = first_line[0]
width = int(first_line[1])

# Read all remaining lines
for line in sys.stdin:
    line = line.rstrip('\n')
    
    if alignment == 'left':
        output = line.ljust(width)
    elif alignment == 'right':
        output = line.rjust(width)
    elif alignment == 'center':
        output = line.center(width)
    
    print(output)