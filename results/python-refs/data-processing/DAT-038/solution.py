import sys

# Define log level hierarchy
log_levels = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']

# Read input
lines = sys.stdin.read().strip().split('\n')
min_level = lines[0]
log_lines = lines[1:]

# Get minimum level index
min_level_idx = log_levels.index(min_level)

# Filter and count
matching_lines = []
counts = {}

for line in log_lines:
    # Find log level in the line
    for level in log_levels:
        if level in line:
            level_idx = log_levels.index(level)
            if level_idx >= min_level_idx:
                matching_lines.append(line)
                counts[level] = counts.get(level, 0) + 1
            break

# Output matching lines
for line in matching_lines:
    print(line)

# Output separator
print('---')

# Output counts in order of log level hierarchy
for level in log_levels:
    if level in counts:
        print(f'{level}: {counts[level]}')