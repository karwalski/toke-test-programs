import sys
import re
from collections import defaultdict

def parse_log_line(line):
    # Parse Apache Combined Log Format
    # Extract timestamp and status code
    pattern = r'\[([^\]]+)\] "[^"]*" (\d+)'
    match = re.search(pattern, line.strip())
    
    if match:
        timestamp_str = match.group(1)
        status_code = match.group(2)
        
        # Extract hour from timestamp (format: 10/Oct/2000:13:00:01 +0000)
        time_pattern = r'\d+/\w+/\d+:(\d+):(\d+):\d+'
        time_match = re.search(time_pattern, timestamp_str)
        
        if time_match:
            hour = time_match.group(1)
            minute = time_match.group(2)
            hour_minute = f"{hour}:{minute}"
            return hour_minute, status_code
    
    return None, None

# Count occurrences
counts = defaultdict(int)

# Read from stdin
for line in sys.stdin:
    hour_minute, status_code = parse_log_line(line)
    if hour_minute and status_code:
        counts[(hour_minute, status_code)] += 1

# Sort and output
for (hour_minute, status_code), count in sorted(counts.items()):
    print(f"{hour_minute}  {status_code}  {count}")