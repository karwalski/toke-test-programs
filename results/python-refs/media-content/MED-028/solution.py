import sys

# Read column width
width = int(input())

# Read and process remaining lines
for line in sys.stdin:
    line = line.rstrip('\n')
    
    # Hard-wrap the line at the given width
    while len(line) > width:
        print(line[:width])
        line = line[width:]
    
    # Print the remaining part (if any)
    if line:
        print(line)