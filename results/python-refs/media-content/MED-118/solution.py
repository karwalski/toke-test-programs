import sys
from datetime import datetime

def parse_ics():
    events = []
    current_event = {}
    
    for line in sys.stdin:
        line = line.strip()
        
        if line == "BEGIN:VEVENT":
            current_event = {}
        elif line == "END:VEVENT":
            if 'DTSTART' in current_event and 'SUMMARY' in current_event:
                events.append(current_event)
        elif line.startswith("DTSTART:"):
            dt_str = line[8:]  # Remove "DTSTART:"
            if dt_str.endswith('Z'):
                dt_str = dt_str[:-1]  # Remove 'Z'
            dt = datetime.strptime(dt_str, "%Y%m%dT%H%M%S")
            current_event['DTSTART'] = dt
        elif line.startswith("SUMMARY:"):
            current_event['SUMMARY'] = line[8:]  # Remove "SUMMARY:"
    
    # Sort events by date
    events.sort(key=lambda x: x['DTSTART'])
    
    # Output events
    for event in events:
        dt = event['DTSTART']
        date_str = dt.strftime("%Y-%m-%d %H:%M")
        summary = event['SUMMARY']
        print(f"{date_str} | {summary}")

parse_ics()