import sys
from datetime import datetime
import time

def parse_datetime(dt_string):
    # Try common datetime formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(dt_string.strip(), fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse datetime: {dt_string}")

def get_timezone_offset(tz_name, dt):
    if tz_name == "UTC":
        return 0
    
    # Common timezone offsets (in seconds)
    tz_offsets = {
        "Australia/Sydney": 11 * 3600,  # AEDT (UTC+11)
        "Australia/Melbourne": 11 * 3600,  # AEDT (UTC+11)
        "Australia/Perth": 8 * 3600,   # AWST (UTC+8)
        "US/Eastern": -5 * 3600,       # EST (UTC-5)
        "US/Central": -6 * 3600,       # CST (UTC-6)
        "US/Mountain": -7 * 3600,      # MST (UTC-7)
        "US/Pacific": -8 * 3600,       # PST (UTC-8)
        "Europe/London": 0,            # GMT (UTC+0)
        "Europe/Berlin": 1 * 3600,     # CET (UTC+1)
        "Asia/Tokyo": 9 * 3600,        # JST (UTC+9)
        "Asia/Shanghai": 8 * 3600,     # CST (UTC+8)
    }
    
    return tz_offsets.get(tz_name, 0)

def convert_timezone(dt, source_tz, target_tz):
    # Convert to UTC first
    if source_tz == "local":
        # Get local timezone offset
        local_offset = -time.timezone
        utc_timestamp = dt.timestamp() - local_offset
    else:
        source_offset = get_timezone_offset(source_tz, dt)
        utc_timestamp = dt.timestamp() - source_offset
    
    # Convert from UTC to target timezone
    target_offset = get_timezone_offset(target_tz, dt)
    target_timestamp = utc_timestamp + target_offset
    
    target_dt = datetime.fromtimestamp(target_timestamp)
    
    # Format offset for ISO 8601
    offset_hours = target_offset // 3600
    offset_minutes = abs(target_offset % 3600) // 60
    
    if target_offset >= 0:
        offset_str = f"+{offset_hours:02d}:{offset_minutes:02d}"
    else:
        offset_str = f"{offset_hours:03d}:{offset_minutes:02d}"
    
    return target_dt.strftime("%Y-%m-%dT%H:%M:%S") + offset_str

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

dt_string = lines[0]
source_tz = lines[1]
target_tz = lines[2]

# Parse datetime
dt = parse_datetime(dt_string)

# Convert timezone
result = convert_timezone(dt, source_tz, target_tz)

print(f"Converted: {result}")