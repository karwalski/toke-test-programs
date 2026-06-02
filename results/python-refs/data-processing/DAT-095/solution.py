import sys
from datetime import datetime
import re

def parse_date(date_str):
    date_str = date_str.strip()
    
    # Try different date formats
    formats = [
        # DD/MM/YYYY
        ('%d/%m/%Y', r'^\d{1,2}/\d{1,2}/\d{4}$'),
        # MM-DD-YYYY
        ('%m-%d-%Y', r'^\d{1,2}-\d{1,2}-\d{4}$'),
        # YYYY-MM-DD (already ISO format)
        ('%Y-%m-%d', r'^\d{4}-\d{1,2}-\d{1,2}$'),
        # Month DD YYYY
        ('%B %d %Y', r'^[A-Za-z]+ \d{1,2} \d{4}$'),
        # Month DD, YYYY
        ('%B %d, %Y', r'^[A-Za-z]+ \d{1,2}, \d{4}$'),
    ]
    
    for fmt, pattern in formats:
        if re.match(pattern, date_str):
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
    
    return 'INVALID: format not recognised'

# Read from stdin and process each line
for line in sys.stdin:
    line = line.strip()
    if line:  # Skip empty lines
        result = parse_date(line)
        print(result)