import sys
import json
import re

def parse_apache_log(line):
    # Apache combined log format regex
    pattern = r'(\S+) \S+ (\S+) \[([^\]]+)\] "(\S+) (\S+) \S+" (\d+) (\d+)'
    match = re.match(pattern, line)
    
    if match:
        host = match.group(1)
        user = match.group(2) if match.group(2) != '-' else None
        method = match.group(4)
        path = match.group(5)
        status = int(match.group(6))
        bytes_sent = int(match.group(7))
        
        result = {
            "host": host,
            "user": user,
            "method": method,
            "path": path,
            "status": status,
            "bytes": bytes_sent
        }
        
        # Remove None values
        return {k: v for k, v in result.items() if v is not None}
    
    return None

def parse_syslog(line):
    # Basic syslog format: timestamp hostname process[pid]: message
    pattern = r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+([^:\[]+)(?:\[(\d+)\])?\s*:\s*(.*)'
    match = re.match(pattern, line)
    
    if match:
        timestamp = match.group(1)
        hostname = match.group(2)
        process = match.group(3)
        pid = match.group(4)
        message = match.group(5)
        
        result = {
            "timestamp": timestamp,
            "hostname": hostname,
            "process": process,
            "message": message
        }
        
        if pid:
            result["pid"] = int(pid)
        
        return result
    
    return None

# Read input
lines = sys.stdin.read().strip().split('\n')
format_type = lines[0].strip()

# Process each log entry
for line in lines[1:]:
    line = line.strip()
    if not line:
        continue
        
    if format_type == 'apache':
        parsed = parse_apache_log(line)
    elif format_type == 'syslog':
        parsed = parse_syslog(line)
    else:
        continue
    
    if parsed:
        print(json.dumps(parsed, separators=(',', ':')))