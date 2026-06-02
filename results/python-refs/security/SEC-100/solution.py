import json
import sys
from datetime import datetime
from collections import defaultdict

def parse_timestamp(ts_str):
    return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))

def detect_patterns(events):
    patterns = []
    
    # Group events by IP
    events_by_ip = defaultdict(list)
    for event in events:
        events_by_ip[event['ip']].append(event)
    
    # Sort events by timestamp for each IP
    for ip in events_by_ip:
        events_by_ip[ip].sort(key=lambda x: parse_timestamp(x['timestamp']))
    
    # Detect brute force attacks
    for ip, ip_events in events_by_ip.items():
        failed_logins = [e for e in ip_events if e['type'] == 'login_fail']
        
        if len(failed_logins) >= 2:
            # Check if failures are within a reasonable time window (e.g., 5 minutes)
            first_fail = parse_timestamp(failed_logins[0]['timestamp'])
            last_fail = parse_timestamp(failed_logins[-1]['timestamp'])
            time_diff = (last_fail - first_fail).total_seconds()
            
            if time_diff <= 300:  # 5 minutes
                confidence = min(0.9, 0.3 + (len(failed_logins) * 0.1))
                
                pattern = {
                    "attack_type": "brute_force",
                    "confidence": confidence,
                    "involved_ips": [ip],
                    "event_chain": failed_logins,
                    "recommendation": "Block IP and investigate user account"
                }
                patterns.append(pattern)
    
    return patterns

def main():
    events = []
    
    # Read all events from stdin
    for line in sys.stdin:
        line = line.strip()
        if line:
            try:
                event = json.loads(line)
                events.append(event)
            except json.JSONDecodeError:
                continue
    
    # Detect patterns
    detected_patterns = detect_patterns(events)
    
    # Output result
    if detected_patterns:
        print("patterns_detected")

if __name__ == "__main__":
    main()