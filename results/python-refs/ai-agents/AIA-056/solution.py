import json
import re
import sys
from datetime import datetime, timedelta

def parse_input():
    input_data = json.loads(sys.stdin.read().strip())
    return input_data['text'], input_data['reference_date']

def extract_dates_and_times(text, reference_date):
    results = []
    reference_dt = datetime.fromisoformat(reference_date)
    
    # Pattern for absolute dates with times
    absolute_patterns = [
        # March 5th, 2024 at 3pm
        r'(\w+ \d{1,2}(?:st|nd|rd|th)?, \d{4} at \d{1,2}(?::\d{2})?(?:am|pm)?)',
        # 2024-03-05 15:00
        r'(\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2}(?::\d{2})?)?)',
        # March 5, 2024
        r'(\w+ \d{1,2}, \d{4})',
        # 03/05/2024
        r'(\d{1,2}/\d{1,2}/\d{4})',
    ]
    
    # Pattern for relative dates
    relative_patterns = [
        r'(next week)',
        r'(next month)',
        r'(tomorrow)',
        r'(yesterday)',
        r'(today)',
        r'(in \d+ days?)',
        r'(\d+ days? ago)',
    ]
    
    # Find absolute dates
    for pattern in absolute_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            original = match.group(1)
            normalized = normalize_absolute_date(original)
            if normalized:
                results.append({
                    "original": original,
                    "normalised": normalized,
                    "type": "absolute"
                })
    
    # Find relative dates
    for pattern in relative_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            original = match.group(1)
            normalized = normalize_relative_date(original, reference_dt)
            if normalized:
                results.append({
                    "original": original,
                    "normalised": normalized,
                    "type": "relative"
                })
    
    return results

def normalize_absolute_date(date_str):
    months = {
        'january': 1, 'jan': 1,
        'february': 2, 'feb': 2,
        'march': 3, 'mar': 3,
        'april': 4, 'apr': 4,
        'may': 5,
        'june': 6, 'jun': 6,
        'july': 7, 'jul': 7,
        'august': 8, 'aug': 8,
        'september': 9, 'sep': 9, 'sept': 9,
        'october': 10, 'oct': 10,
        'november': 11, 'nov': 11,
        'december': 12, 'dec': 12
    }
    
    # March 5th, 2024 at 3pm
    match = re.match(r'(\w+) (\d{1,2})(?:st|nd|rd|th)?, (\d{4}) at (\d{1,2})(?::(\d{2}))?(\w{2})?', date_str, re.IGNORECASE)
    if match:
        month_name, day, year, hour, minute, ampm = match.groups()
        month = months.get(month_name.lower())
        if month:
            hour = int(hour)
            if ampm and ampm.lower() == 'pm' and hour != 12:
                hour += 12
            elif ampm and ampm.lower() == 'am' and hour == 12:
                hour = 0
            minute = int(minute) if minute else 0
            return f"{year}-{month:02d}-{int(day):02d}T{hour:02d}:{minute:02d}:00"
    
    return None

def normalize_relative_date(date_str, reference_dt):
    if date_str.lower() == 'next week':
        # Next week means 7 days from reference date
        target_date = reference_dt + timedelta(days=7)
        return target_date.strftime('%Y-%m-%d')
    elif date_str.lower() == 'tomorrow':
        target_date = reference_dt + timedelta(days=1)
        return target_date.strftime('%Y-%m-%d')
    elif date_str.lower() == 'yesterday':
        target_date = reference_dt - timedelta(days=1)
        return target_date.strftime('%Y-%m-%d')
    elif date_str.lower() == 'today':
        return reference_dt.strftime('%Y-%m-%d')
    
    return None

def main():
    text, reference_date = parse_input()
    results = extract_dates_and_times(text, reference_date)
    print(json.dumps(results, separators=(',', ':')))

if __name__ == "__main__":
    main()