import sys
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict

def parse_log_line(line):
    # Common log format pattern
    pattern = r'^(\d+\.\d+\.\d+\.\d+) .* \[(.*?)\] ".*?" (\d+)'
    match = re.match(pattern, line)
    if match:
        ip = match.group(1)
        timestamp_str = match.group(2)
        status_code = int(match.group(3))
        
        # Parse timestamp (format: DD/MMM/YYYY:HH:MM:SS +ZZZZ)
        try:
            timestamp = datetime.strptime(timestamp_str.split()[0], '%d/%b/%Y:%H:%M:%S')
            return ip, timestamp, status_code
        except:
            return None
    return None

def analyze_brute_force(log_file_path):
    failed_attempts = defaultdict(list)
    
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                parsed = parse_log_line(line.strip())
                if parsed:
                    ip, timestamp, status_code = parsed
                    # Consider 401, 403 as failed login attempts
                    if status_code in [401, 403]:
                        failed_attempts[ip].append(timestamp)
    except FileNotFoundError:
        return []
    
    suspicious_ips = []
    
    for ip, timestamps in failed_attempts.items():
        if len(timestamps) < 10:
            continue
            
        # Sort timestamps
        timestamps.sort()
        
        # Check for >10 failed attempts within 5 minutes
        for i in range(len(timestamps) - 9):
            window_start = timestamps[i]
            window_end = window_start + timedelta(minutes=5)
            
            count = 0
            last_in_window = window_start
            
            for j in range(i, len(timestamps)):
                if timestamps[j] <= window_end:
                    count += 1
                    last_in_window = timestamps[j]
                else:
                    break
            
            if count > 10:
                # Determine recommendation based on severity
                recommendation = "block" if count > 20 else "monitor"
                
                suspicious_ips.append({
                    "ip": ip,
                    "failedAttempts": count,
                    "firstSeen": window_start.strftime("%Y-%m-%d %H:%M:%S"),
                    "lastSeen": last_in_window.strftime("%Y-%m-%d %H:%M:%S"),
                    "recommendation": recommendation
                })
                break
    
    return suspicious_ips

# Read input
log_file_path = input().strip()

# Analyze and output
result = analyze_brute_force(log_file_path)
print("[")