import sys
import json
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import statistics

def parse_log_line(line):
    """Parse a single log line in Combined Log Format"""
    # Combined Log Format regex
    pattern = r'(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d+) (\d+) "([^"]*)" "([^"]*)"'
    match = re.match(pattern, line)
    
    if not match:
        return None
    
    ip, timestamp, method, path, protocol, status, size, referer, user_agent = match.groups()
    
    # Parse timestamp
    try:
        dt = datetime.strptime(timestamp.split()[0], '%d/%b/%Y:%H:%M:%S')
        return {
            'ip': ip,
            'timestamp': dt,
            'method': method,
            'path': path,
            'protocol': protocol,
            'status': int(status),
            'size': int(size) if size != '-' else 0,
            'referer': referer,
            'user_agent': user_agent
        }
    except:
        return None

def is_suspicious_user_agent(ua):
    """Check if user agent is suspicious"""
    suspicious_patterns = [
        r'sqlmap',
        r'nmap',
        r'nikto',
        r'dirbuster',
        r'gobuster',
        r'masscan',
        r'python-requests',
        r'wget',
        r'curl/\d+\.\d+$',
        r'^-$',
        r'scanner',
        r'bot.*exploit',
        r'hack',
        r'injection'
    ]
    
    ua_lower = ua.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, ua_lower):
            return True
    return False

def is_path_traversal(path):
    """Check if path contains traversal attempts"""
    traversal_patterns = [
        r'\.\./.*\.\./',
        r'\.\.\\.*\.\.\\',
        r'%2e%2e%2f',
        r'%2e%2e\\',
        r'\.\.%2f',
        r'\.\./',
        r'\.\.\\'
    ]
    
    path_lower = path.lower()
    for pattern in traversal_patterns:
        if re.search(pattern, path_lower):
            return True
    return False

def analyze_logs(log_file_path, window_hours):
    """Analyze logs for security issues"""
    
    # Try to read the log file, if it doesn't exist, return empty results
    try:
        with open(log_file_path, 'r') as f:
            lines = f.readlines()
    except:
        lines = []
    
    # Calculate time window
    cutoff_time = datetime.now() - timedelta(hours=window_hours)
    
    # Data structures for analysis
    ip_counts = Counter()
    user_agents = defaultdict(int)
    traversal_attempts = []
    ip_request_times = defaultdict(list)
    
    # Process each log line
    for line in lines:
        entry = parse_log_line(line.strip())
        if not entry:
            continue
        
        # Skip entries outside time window
        if entry['timestamp'] < cutoff_time:
            continue
        
        # Count IPs
        ip_counts[entry['ip']] += 1
        
        # Track request times for rate analysis
        ip_request_times[entry['ip']].append(entry['timestamp'])
        
        # Check for suspicious user agents
        if is_suspicious_user_agent(entry['user_agent']):
            user_agents[entry['user_agent']] += 1
        
        # Check for path traversal
        if is_path_traversal(entry['path']):
            traversal_attempts.append({
                'ip': entry['ip'],
                'path': entry['path'],
                'timestamp': entry['timestamp'].isoformat(),
                'user_agent': entry['user_agent']
            })
    
    # Get top IPs (top 10)
    top_ips = [{'ip': ip, 'count': count} for ip, count in ip_counts.most_common(10)]
    
    # Get suspicious user agents (top 10)
    suspicious_agents = [{'user_agent': ua, 'count': count} for ua, count in 
                        Counter(user_agents).most_common(10)]
    
    # Detect rate anomalies
    rate_anomalies = []
    for ip, timestamps in ip_request_times.items():
        if len(timestamps) < 2:
            continue
        
        # Calculate requests per minute
        timestamps.sort()
        duration = (timestamps[-1] - timestamps[0]).total_seconds() / 60.0
        if duration > 0:
            rate = len(timestamps) / duration
            # Flag IPs with > 10 requests per minute
            if rate > 10:
                rate_anomalies.append({
                    'ip': ip,
                    'rate_per_minute': round(rate, 2),
                    'total_requests': len(timestamps)
                })
    
    # Sort rate anomalies by rate
    rate_anomalies.sort(key=lambda x: x['rate_per_minute'], reverse=True)
    
    # Create summary
    summary = {
        'total_unique_ips': len(ip_counts),
        'total_requests': sum(ip_counts.values()),
        'suspicious_agents_count': len(suspicious_agents),
        'traversal_attempts_count': len(traversal_attempts),
        'rate_anomalies_count': len(rate_anomalies),
        'analysis_window_hours': window_hours
    }
    
    return {
        'top_ips': top_ips,
        'suspicious_agents': suspicious_agents,
        'traversal_attempts': traversal_attempts,
        'rate_anomalies': rate_anomalies,
        'summary': summary
    }

def main():
    # Read input from stdin
    log_file_path = input().strip()
    window_hours = int(input().strip())
    
    # Analyze logs
    result = analyze_logs(log_file_path, window_hours)
    
    # Output JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()