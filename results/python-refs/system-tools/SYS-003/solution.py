import sys
from datetime import datetime, timedelta

def parse_cron_field(field, min_val, max_val):
    """Parse a single cron field and return list of valid values"""
    if field == '*':
        return list(range(min_val, max_val + 1))
    
    values = []
    for part in field.split(','):
        if '/' in part:
            range_part, step = part.split('/')
            step = int(step)
            if range_part == '*':
                start, end = min_val, max_val
            elif '-' in range_part:
                start, end = map(int, range_part.split('-'))
            else:
                start = end = int(range_part)
            values.extend(range(start, end + 1, step))
        elif '-' in part:
            start, end = map(int, part.split('-'))
            values.extend(range(start, end + 1))
        else:
            values.append(int(part))
    
    return sorted(set(v for v in values if min_val <= v <= max_val))

def parse_cron_expression(cron_expr):
    """Parse cron expression and return (minutes, hours, days, months, weekdays)"""
    fields = cron_expr.split()
    if len(fields) != 5:
        raise ValueError("Invalid cron expression")
    
    minutes = parse_cron_field(fields[0], 0, 59)
    hours = parse_cron_field(fields[1], 0, 23)
    days = parse_cron_field(fields[2], 1, 31)
    months = parse_cron_field(fields[3], 1, 12)
    weekdays = parse_cron_field(fields[4], 0, 7)  # 0 and 7 are both Sunday
    
    # Normalize Sunday (7 -> 0)
    weekdays = [0 if w == 7 else w for w in weekdays]
    weekdays = sorted(set(weekdays))
    
    return minutes, hours, days, months, weekdays

def get_next_times(cron_expr, n, start_time=None):
    """Get next N times for a cron expression"""
    if start_time is None:
        start_time = datetime.now()
    
    minutes, hours, days, months, weekdays = parse_cron_expression(cron_expr)
    
    times = []
    current = start_time.replace(second=0, microsecond=0)
    current += timedelta(minutes=1)  # Start from next minute
    
    max_iterations = 366 * 24 * 60  # Prevent infinite loops
    iterations = 0
    
    while len(times) < n and iterations < max_iterations:
        iterations += 1
        
        if (current.minute in minutes and
            current.hour in hours and
            current.month in months):
            
            # Check day of month OR day of week (cron uses OR logic)
            day_match = current.day in days
            weekday_match = current.weekday() in [(w + 6) % 7 for w in weekdays]  # Convert to Python weekday
            
            if day_match or weekday_match:
                times.append(current)
        
        current += timedelta(minutes=1)
    
    return times

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    if len(lines) < 2:
        return
    
    schedule_line = lines[0]
    n = int(lines[1])
    
    # Parse schedule line: "CRON_EXPR label"
    parts = schedule_line.split()
    if len(parts) < 6:
        return
    
    cron_expr = ' '.join(parts[:5])
    label = ' '.join(parts[5:])
    
    # Get next N scheduled times
    next_times = get_next_times(cron_expr, n)
    
    # Format output
    time_strs = [t.strftime('%Y-%m-%dT%H:%M:%S') for t in next_times]
    print(f"{label}: {', '.join(time_strs)}")

if __name__ == "__main__":
    main()