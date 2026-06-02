import sys

def parse_cron():
    line = sys.stdin.read().strip()
    fields = line.split()
    
    if len(fields) != 5:
        return "Invalid cron expression"
    
    minute, hour, dom, month, dow = fields
    
    # Parse time
    time_parts = []
    
    # Handle minute
    if minute == "0":
        min_str = "00"
    elif minute.isdigit():
        min_str = f"{int(minute):02d}"
    else:
        min_str = minute
    
    # Handle hour
    if hour.isdigit():
        hour_str = f"{int(hour):02d}"
    else:
        hour_str = hour
    
    # Build time string
    if minute == "0" and hour.isdigit():
        time_str = f"At {hour_str}:00"
    else:
        time_str = f"At {hour_str}:{min_str}"
    
    # Parse day of week
    dow_names = {
        '0': 'Sunday', '1': 'Monday', '2': 'Tuesday', '3': 'Wednesday',
        '4': 'Thursday', '5': 'Friday', '6': 'Saturday', '7': 'Sunday'
    }
    
    dow_parts = []
    
    if dow == "*":
        dow_str = ""
    elif "-" in dow:
        start, end = dow.split("-")
        if start == "1" and end == "5":
            dow_str = "Monday through Friday"
        else:
            start_name = dow_names.get(start, start)
            end_name = dow_names.get(end, end)
            dow_str = f"{start_name} through {end_name}"
    elif "," in dow:
        days = dow.split(",")
        day_names = [dow_names.get(d, d) for d in days]
        if len(day_names) == 2:
            dow_str = f"{day_names[0]} and {day_names[1]}"
        else:
            dow_str = ", ".join(day_names[:-1]) + f", and {day_names[-1]}"
    elif dow.isdigit():
        dow_str = dow_names.get(dow, dow)
    else:
        dow_str = dow
    
    # Combine time and day
    if dow_str:
        result = f"{time_str}, {dow_str}"
    else:
        result = time_str
    
    return result

print(parse_cron())