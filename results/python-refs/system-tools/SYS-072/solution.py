import sys

# Read the first line to get output file paths
file_paths_line = input().strip()

# Parse file paths (empty string means stdout only)
if file_paths_line:
    file_paths = [path.strip() for path in file_paths_line.split(',')]
else:
    file_paths = []

# Open all output files
output_files = []
for path in file_paths:
    output_files.append(open(path, 'w'))

try:
    # Read remaining lines and write to stdout and files
    for line in sys.stdin:
        # Write to stdout
        print(line, end='')
        
        # Write to all output files
        for f in output_files:
            f.write(line)
            f.flush()
            
finally:
    # Close all files
    for f in output_files:
        f.close()