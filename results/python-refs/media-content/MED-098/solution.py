import sys
from datetime import datetime

def parse_date(date_str):
    """Parse a date string and return a datetime object"""
    date_str = date_str.strip()
    
    # Try different input formats
    formats = [
        "%m/%d/%Y",    # US format: 01/15/2024
        "%d.%m.%Y",    # EU format: 15.01.2024
        "%Y-%m-%d",    # ISO format: 2024-01-15
        "%B %d, %Y",   # Long format: January 15, 2024
        "%d/%m/%Y",    # Alternative EU: 15/01/2024
        "%m-%d-%Y",    # Alternative US: 01-15-2024
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")

def format_date(dt, target_format):
    """Format a datetime object according to target format"""
    if target_format == "ISO":
        return dt.strftime("%Y-%m-%d")
    elif target_format == "US":
        return dt.strftime("%m/%d/%Y")
    elif target_format == "EU":
        return dt.strftime("%d.%m.%Y")
    elif target_format == "LONG":
        return dt.strftime("%B %d, %Y")
    else:
        raise ValueError(f"Unknown target format: {target_format}")

# Read input
lines = sys.stdin.read().strip().split('\n')
target_format = lines[0]

# Process each date
for i in range(1, len(lines)):
    date_str = lines[i]
    try:
        dt = parse_date(date_str)
        converted = format_date(dt, target_format)
        print(converted)
    except ValueError:
        # Skip invalid dates
        pass