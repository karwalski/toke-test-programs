import json
import sys
from datetime import datetime

def parse_iso_time(time_str):
    return datetime.fromisoformat(time_str.replace('Z', '+00:00'))

def format_duration(minutes):
    if minutes == 0:
        return "0m"
    return f"{minutes}m"

def format_time(dt):
    return dt.strftime("%H:%M")

def main():
    lines = sys.stdin.read().strip().split('\n')
    report_time_str = lines[0]
    events_json = lines[1]
    
    report_time = parse_iso_time(report_time_str)
    events = json.loads(events_json)
    
    # Sort events by time
    events.sort(key=lambda x: parse_iso_time(x['time']))
    
    users = {}
    
    for event in events:
        user = event['user']
        status = event['status']
        time = parse_iso_time(event['time'])
        
        if user not in users:
            users[user] = {
                'current_status': status,
                'last_change': time,
                'durations': {'online': 0, 'offline': 0, 'away': 0},
                'events': []
            }
        
        users[user]['events'].append((time, status))
    
    # Calculate durations for each user
    for user, data in users.items():
        events = data['events']
        durations = {'online': 0, 'offline': 0, 'away': 0}
        
        if not events:
            continue
            
        current_status = None
        current_start = None
        
        for event_time, status in events:
            # If we have a previous status, calculate its duration
            if current_status is not None:
                duration_minutes = int((event_time - current_start).total_seconds() / 60)
                durations[current_status] += duration_minutes
            
            current_status = status
            current_start = event_time
        
        # Calculate duration from last status change to report time
        if current_status is not None:
            duration_minutes = int((report_time - current_start).total_seconds() / 60)
            durations[current_status] += duration_minutes
        
        data['current_status'] = current_status
        data['last_change'] = current_start
        data['durations'] = durations
    
    # Generate output
    for user in sorted(users.keys()):
        data = users[user]
        current_status = data['current_status']
        last_change = data['last_change']
        durations = data['durations']
        
        # Build duration string
        duration_parts = []
        for status in ['online', 'offline', 'away']:
            if durations[status] > 0:
                duration_parts.append(f"{status}: {format_duration(durations[status])}")
        
        duration_str = ", ".join(duration_parts)
        
        print(f"{user}: {current_status} (since {format_time(last_change)}, {duration_str})")

if __name__ == "__main__":
    main()