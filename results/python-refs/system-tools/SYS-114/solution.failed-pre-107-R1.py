import sys
import re
from datetime import datetime
from collections import defaultdict

def main():
    # Read input
    log_file_path = input().strip()
    timestamp_regex = input().strip()
    bucket_type = input().strip()
    
    # Compile regex
    pattern = re.compile(timestamp_regex)
    
    # Parse log file and extract timestamps
    timestamps = []
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    timestamp_str = match.group(0)
                    try:
                        # Parse ISO format timestamp
                        dt = datetime.fromisoformat(timestamp_str)
                        timestamps.append(dt)
                    except ValueError:
                        continue
    except FileNotFoundError:
        # If file doesn't exist, exit silently
        return
    
    if not timestamps:
        return
    
    # Group by bucket
    bucket_counts = defaultdict(int)
    
    for dt in timestamps:
        if bucket_type == "second":
            bucket_key = dt.strftime("%Y-%m-%dT%H:%M:%S")
        elif bucket_type == "minute":
            bucket_key = dt.strftime("%Y-%m-%dT%H:%M:00")
        elif bucket_type == "hour":
            bucket_key = dt.strftime("%Y-%m-%dT%H:00:00")
        
        bucket_counts[bucket_key] += 1
    
    # Sort by timestamp and output
    for bucket_start in sorted(bucket_counts.keys()):
        print(f"{bucket_start} {bucket_counts[bucket_start]}")

if __name__ == "__main__":
    main()