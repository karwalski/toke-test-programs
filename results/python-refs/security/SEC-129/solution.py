import sys
import re
from datetime import datetime, timedelta
from typing import List, Tuple, Dict

def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse various timestamp formats commonly found in logs"""
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%b %d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%d/%b/%Y:%H:%M:%S %z",
        "%d/%b/%Y:%H:%M:%S"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    
    # Handle syslog format (assume current year if not present)
    try:
        dt = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
        return dt.replace(year=datetime.now().year)
    except ValueError:
        pass
    
    return None

def calculate_relevance_score(event_text: str) -> int:
    """Calculate relevance score based on security keywords"""
    high_priority = ['failed', 'error', 'denied', 'attack', 'breach', 'unauthorized', 'suspicious', 'alert']
    medium_priority = ['warning', 'authentication', 'login', 'logout', 'access', 'connection']
    low_priority = ['info', 'debug', 'notice']
    
    event_lower = event_text.lower()
    
    for keyword in high_priority:
        if keyword in event_lower:
            return 3
    
    for keyword in medium_priority:
        if keyword in event_lower:
            return 2
    
    for keyword in low_priority:
        if keyword in event_lower:
            return 1
    
    return 1

def parse_log_line(line: str, source: str) -> Tuple[datetime, str, str, int]:
    """Parse a single log line and extract timestamp, event, and relevance"""
    line = line.strip()
    if not line:
        return None
    
    # Try to extract timestamp from beginning of line
    timestamp_patterns = [
        r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?)',
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',
        r'(\w{3} \d{1,2} \d{2}:\d{2}:\d{2})',
        r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})',
    ]
    
    timestamp = None
    event = line
    
    for pattern in timestamp_patterns:
        match = re.match(pattern, line)
        if match:
            timestamp_str = match.group(1)
            timestamp = parse_timestamp(timestamp_str)
            if timestamp:
                event = line[len(timestamp_str):].strip()
                break
    
    if not timestamp:
        return None
    
    relevance_score = calculate_relevance_score(event)
    
    return timestamp, source, event, relevance_score

def main():
    # Read incident timestamp
    incident_time_str = input().strip()
    incident_time = parse_timestamp(incident_time_str)
    
    # Read window minutes
    window_minutes = int(input().strip())
    
    # Calculate time window
    start_time = incident_time - timedelta(minutes=window_minutes)
    end_time = incident_time + timedelta(minutes=window_minutes)
    
    # Read log file paths
    log_files = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            log_files.append(line)
        except EOFError:
            break
    
    # Collect events from all log files
    events = []
    
    for log_file in log_files:
        try:
            with open(log_file, 'r') as f:
                source = log_file.split('/')[-1]  # Extract filename
                for line in f:
                    parsed = parse_log_line(line, source)
                    if parsed:
                        timestamp, src, event, score = parsed
                        if start_time <= timestamp <= end_time:
                            events.append((timestamp, src, event, score))
        except FileNotFoundError:
            continue
    
    # Sort events by timestamp
    events.sort(key=lambda x: x[0])
    
    # Output timeline
    print("Timeline")
    
    for timestamp, source, event, relevance_score in events:
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        highlight = "*" if relevance_score >= 3 else ""
        print(f"{highlight}{timestamp_str}, {source}, {event}, {relevance_score}")

if __name__ == "__main__":
    main()