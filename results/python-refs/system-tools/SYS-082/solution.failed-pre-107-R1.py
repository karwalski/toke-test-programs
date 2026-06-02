import sys
import re
from datetime import datetime

def parse_timestamp(line, pattern):
    """Extract timestamp from log line using the given pattern."""
    match = re.search(pattern, line)
    if match:
        timestamp_str = match.group(0)
        try:
            # Try to parse the timestamp in ISO format
            return datetime.fromisoformat(timestamp_str.replace('T', ' '))
        except:
            try:
                # Try common timestamp formats
                formats = [
                    '%Y-%m-%dT%H:%M:%S',
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d_%H:%M:%S',
                    '%d/%m/%Y %H:%M:%S',
                    '%m/%d/%Y %H:%M:%S'
                ]
                for fmt in formats:
                    try:
                        return datetime.strptime(timestamp_str, fmt)
                    except:
                        continue
            except:
                pass
    return None

def main():
    lines = sys.stdin.read().strip().split('\n')
    timestamp_pattern = lines[0]
    log_files = lines[1:]
    
    all_log_entries = []
    seen_lines = set()
    
    # Read all log files
    for file_path in log_files:
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.rstrip('\n')
                    if line and line not in seen_lines:
                        timestamp = parse_timestamp(line, timestamp_pattern)
                        if timestamp:
                            all_log_entries.append((timestamp, line))
                            seen_lines.add(line)
        except FileNotFoundError:
            # Skip files that don't exist
            continue
        except Exception:
            # Skip files that can't be read
            continue
    
    # Sort by timestamp
    all_log_entries.sort(key=lambda x: x[0])
    
    # Output the merged log lines
    for _, line in all_log_entries:
        print(line)

if __name__ == "__main__":
    main()