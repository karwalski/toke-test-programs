import sys
from datetime import datetime, timedelta

# Read window size
window_size_minutes = int(input().strip())

# Parse log entries
log_entries = []
for line in sys.stdin:
    line = line.strip()
    if line:
        # Extract timestamp (first 19 characters for ISO format)
        timestamp_str = line[:19]
        timestamp = datetime.fromisoformat(timestamp_str)
        log_entries.append(timestamp)

# Group entries by time windows
windows = {}
for timestamp in log_entries:
    # Calculate window start time
    minutes_since_midnight = timestamp.hour * 60 + timestamp.minute
    window_start_minutes = (minutes_since_midnight // window_size_minutes) * window_size_minutes
    
    window_start = timestamp.replace(
        hour=window_start_minutes // 60,
        minute=window_start_minutes % 60,
        second=0,
        microsecond=0
    )
    
    if window_start not in windows:
        windows[window_start] = 0
    windows[window_start] += 1

# Sort windows by time and output
for window_start in sorted(windows.keys()):
    count = windows[window_start]
    print(f"{window_start.strftime('%Y-%m-%d %H:%M')}: {count} events")