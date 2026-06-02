import sys
import urllib.request
import statistics
from collections import defaultdict

def parse_server_timing(header_value):
    """Parse Server-Timing header value and return dict of phase -> time in ms"""
    phases = {}
    if not header_value:
        return phases
    
    # Split by comma to get individual timing entries
    entries = header_value.split(',')
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
            
        # Parse each entry: name;dur=123.45 or name;dur=123.45;desc="description"
        parts = entry.split(';')
        if len(parts) < 2:
            continue
            
        name = parts[0].strip()
        
        # Look for dur= parameter
        for part in parts[1:]:
            part = part.strip()
            if part.startswith('dur='):
                try:
                    duration = float(part[4:])
                    phases[name] = duration
                    break
                except ValueError:
                    continue
    
    return phases

def main():
    # Read input
    url = input().strip()
    n = int(input().strip())
    
    # Collect timing data
    all_phases = defaultdict(list)
    
    for _ in range(n):
        try:
            with urllib.request.urlopen(url) as response:
                server_timing = response.headers.get('Server-Timing', '')
                phases = parse_server_timing(server_timing)
                
                for phase_name, duration in phases.items():
                    all_phases[phase_name].append(duration)
        except Exception:
            # Skip failed requests
            continue
    
    # Calculate statistics and prepare output
    results = []
    for phase_name, durations in all_phases.items():
        if durations:
            min_time = min(durations)
            mean_time = statistics.mean(durations)
            max_time = max(durations)
            results.append((phase_name, min_time, mean_time, max_time))
    
    # Sort by mean descending
    results.sort(key=lambda x: x[2], reverse=True)
    
    # Output table
    if results:
        print(f"{'Phase':<20} {'Min':<10} {'Mean':<10} {'Max':<10}")
        print("-" * 52)
        for phase_name, min_time, mean_time, max_time in results:
            print(f"{phase_name:<20} {min_time:<10.2f} {mean_time:<10.2f} {max_time:<10.2f}")
    else:
        print("Phase")

if __name__ == "__main__":
    main()