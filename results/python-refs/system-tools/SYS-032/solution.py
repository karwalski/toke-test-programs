import sys

# Read input
lines = sys.stdin.read().strip().split('\n')

# Parse input
min_level = lines[0].strip()
keyword = lines[1].strip() if len(lines) > 1 else ""
log_lines = lines[2:] if len(lines) > 2 else []

# Define log level hierarchy
level_priority = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3}
min_priority = level_priority[min_level]

# Filter log lines
for line in log_lines:
    # Extract log level from line
    parts = line.split()
    if len(parts) < 3:
        continue
    
    log_level = parts[1]
    
    # Check if log level meets minimum requirement
    if log_level in level_priority and level_priority[log_level] >= min_priority:
        # Check keyword filter
        if not keyword or keyword in line:
            print(line)