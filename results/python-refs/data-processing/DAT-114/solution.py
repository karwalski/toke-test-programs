import sys
from datetime import datetime
import zoneinfo

# Read timezone information
source_tz, target_tz = input().split()

# Convert timezone strings to timezone objects
source_zone = zoneinfo.ZoneInfo(source_tz)
target_zone = zoneinfo.ZoneInfo(target_tz)

# Process each timestamp
for line in sys.stdin:
    timestamp_str = line.strip()
    if not timestamp_str:
        continue
    
    # Parse the ISO timestamp
    if timestamp_str.endswith('Z'):
        # UTC timestamp
        dt = datetime.fromisoformat(timestamp_str[:-1]).replace(tzinfo=source_zone)
    else:
        dt = datetime.fromisoformat(timestamp_str).replace(tzinfo=source_zone)
    
    # Convert to target timezone
    converted_dt = dt.astimezone(target_zone)
    
    # Format as ISO 8601 with timezone offset
    print(converted_dt.isoformat())