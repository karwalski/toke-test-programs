import sys

# Define severity levels with their numeric values
severity_levels = {
    'DEBUG': 1,
    'INFO': 2,
    'WARN': 3,
    'ERROR': 4,
    'FATAL': 5
}

# Read all input
lines = sys.stdin.read().strip().split('\n')

# Get minimum level from first line
min_level = lines[0]
min_level_value = severity_levels[min_level]

# Process each log line
for i in range(1, len(lines)):
    log_line = lines[i]
    
    # Extract the severity level from the log line
    # Format appears to be: "date level message"
    parts = log_line.split(' ', 2)
    if len(parts) >= 2:
        level = parts[1]
        if level in severity_levels:
            level_value = severity_levels[level]
            if level_value >= min_level_value:
                print(log_line)