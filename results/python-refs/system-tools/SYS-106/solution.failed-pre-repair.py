import sys
import subprocess
import os

def get_log_lines(lines_back, service_filter=None, min_level=None):
    # Try journalctl first (systemd systems)
    try:
        cmd = ['journalctl', '-n', str(lines_back), '--no-pager']
        if service_filter:
            cmd.extend(['-u', service_filter])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            return filter_by_level(lines, min_level)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Fall back to traditional syslog files
    syslog_paths = ['/var/log/syslog', '/var/log/messages', '/var/log/system.log']
    
    for path in syslog_paths:
        if os.path.exists(path):
            try:
                # Use tail command to get last N lines
                result = subprocess.run(['tail', '-n', str(lines_back), path], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    filtered = filter_by_service(lines, service_filter)
                    return filter_by_level(filtered, min_level)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
    
    return []

def filter_by_service(lines, service_filter):
    if not service_filter:
        return lines
    
    filtered = []
    for line in lines:
        if service_filter.lower() in line.lower():
            filtered.append(line)
    return filtered

def filter_by_level(lines, min_level):
    if not min_level:
        return lines
    
    level_priority = {
        'emerg': 0, 'alert': 1, 'crit': 2, 'err': 3,
        'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
    }
    
    min_priority = level_priority.get(min_level.lower(), 7)
    
    filtered = []
    for line in lines:
        line_lower = line.lower()
        for level, priority in level_priority.items():
            if level in line_lower and priority <= min_priority:
                filtered.append(line)
                break
        else:
            # If no level found in line, include it
            if min_level.lower() == 'debug':
                filtered.append(line)
    
    return filtered

def main():
    # Read all input from stdin
    input_data = sys.stdin.read().strip()
    lines = input_data.split('\n')
    
    # Parse input
    lines_back = int(lines[0]) if len(lines) > 0 and lines[0] else 10
    service = lines[1].strip() if len(lines) > 1 and lines[1].strip() else None
    min_level = lines[2].strip() if len(lines) > 2 and lines[2].strip() else None
    
    # Get log lines
    log_lines = get_log_lines(lines_back, service, min_level)
    
    # Output results
    for line in log_lines:
        print(line)

if __name__ == "__main__":
    main()