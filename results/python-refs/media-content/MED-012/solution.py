import sys
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_rss_date(date_str):
    # Parse RFC 2822 format date
    try:
        # Remove timezone info for parsing
        if '+' in date_str:
            date_str = date_str.split('+')[0].strip()
        elif date_str.endswith(' GMT'):
            date_str = date_str[:-4].strip()
        
        # Parse the date
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S")
        return dt.strftime("%Y-%m-%d")
    except:
        return None

# Read XML from stdin
xml_content = sys.stdin.read()

# Parse XML
root = ET.fromstring(xml_content)

# Extract items
items = []
for item in root.findall('.//item'):
    title_elem = item.find('title')
    pubdate_elem = item.find('pubDate')
    
    if title_elem is not None and pubdate_elem is not None:
        title = title_elem.text
        pubdate_str = pubdate_elem.text
        
        parsed_date = parse_rss_date(pubdate_str)
        if parsed_date:
            items.append((parsed_date, title))

# Sort by date (newest first)
items.sort(key=lambda x: x[0], reverse=True)

# Output
for date, title in items:
    print(f"{date} | {title}")