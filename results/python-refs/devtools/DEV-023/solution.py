import sys
from datetime import datetime

def parse_timestamp(timestamp_str):
    """Parse timestamp string to milliseconds since midnight"""
    time_part = timestamp_str.split('.')[0]  # HH:MM:SS
    ms_part = timestamp_str.split('.')[1]    # mmm
    
    h, m, s = map(int, time_part.split(':'))
    ms = int(ms_part)
    
    total_ms = h * 3600000 + m * 60000 + s * 1000 + ms
    return total_ms

def main():
    phase_times = {}
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split(' ', 2)
        timestamp = parts[0]
        phase_and_action = parts[1]
        action = parts[2]
        
        phase_name = phase_and_action[:-1]  # Remove the ':'
        
        ms = parse_timestamp(timestamp)
        
        if phase_name not in phase_times:
            phase_times[phase_name] = {}
            
        phase_times[phase_name][action] = ms
    
    # Calculate durations
    durations = []
    total_duration = 0
    
    for phase_name, times in phase_times.items():
        if 'start' in times and 'end' in times:
            duration = times['end'] - times['start']
            durations.append((phase_name, duration))
            total_duration += duration
    
    # Sort by duration descending
    durations.sort(key=lambda x: x[1], reverse=True)
    
    # Output results
    for phase_name, duration in durations:
        print(f"{phase_name}: {duration}ms")
    
    print(f"Total: {total_duration}ms")

if __name__ == "__main__":
    main()