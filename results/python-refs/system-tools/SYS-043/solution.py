import sys

def parse_cron_field(field, field_type):
    """Parse a single cron field and return human-readable description"""
    if field == '*':
        return None
    
    # Handle specific values
    if field.isdigit():
        num = int(field)
        if field_type == 'minute':
            return f":{num:02d}"
        elif field_type == 'hour':
            return f"{num}:00"
        elif field_type == 'day':
            return f"on day {num}"
        elif field_type == 'month':
            months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
            return f"in {months[num]}"
        elif field_type == 'weekday':
            days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            return f"on {days[num]}"
    
    return None

def describe_cron_schedule(minute, hour, day, month, weekday):
    """Convert cron fields to human-readable description"""
    parts = []
    
    # Check for simple patterns first
    if minute == '0' and hour == '*' and day == '*' and month == '*' and weekday == '*':
        return "every hour at :00"
    
    if minute.isdigit() and hour.isdigit() and day == '*' and month == '*' and weekday == '*':
        return f"every day at {int(hour)}:{int(minute):02d}"
    
    if minute.isdigit() and hour == '*' and day == '*' and month == '*' and weekday == '*':
        return f"every hour at :{int(minute):02d}"
    
    # Build description from parts
    time_parts = []
    schedule_parts = []
    
    if minute != '*':
        time_parts.append(f":{int(minute):02d}")
    else:
        time_parts.append(":00")
    
    if hour != '*':
        time_parts.insert(0, str(int(hour)))
    
    if day != '*':
        schedule_parts.append(f"on day {int(day)}")
    
    if month != '*':
        months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
        schedule_parts.append(f"in {months[int(month)]}")
    
    if weekday != '*':
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        schedule_parts.append(f"on {days[int(weekday)]}")
    
    # Construct final description
    if hour == '*' and minute == '0':
        base = "every hour"
    elif hour == '*':
        base = "every hour"
    elif day == '*' and month == '*' and weekday == '*':
        base = "every day"
    else:
        base = ""
    
    if time_parts and (hour != '*' or minute != '0'):
        if base:
            result = f"{base} at {''.join(time_parts)}"
        else:
            result = f"at {''.join(time_parts)}"
    else:
        result = base
    
    if schedule_parts:
        if result:
            result = f"{result} {' '.join(schedule_parts)}"
        else:
            result = ' '.join(schedule_parts)
    
    return result if result else "every minute"

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        parts = line.split(None, 5)
        if len(parts) < 6:
            continue
        
        minute, hour, day, month, weekday, command = parts
        description = describe_cron_schedule(minute, hour, day, month, weekday)
        print(f"{command}: {description}")

if __name__ == "__main__":
    main()