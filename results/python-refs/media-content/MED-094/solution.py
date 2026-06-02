import sys
import re

def format_phone_number(phone_str):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone_str.strip())
    
    # Check if it's a valid US/Canada number (11 digits starting with 1)
    if len(digits) == 11 and digits[0] == '1':
        country_code = digits[0]
        area_code = digits[1:4]
        exchange = digits[4:7]
        number = digits[7:11]
        return f"+{country_code} ({area_code}) {exchange}-{number}"
    
    # Check if it's a valid US/Canada number without country code (10 digits)
    elif len(digits) == 10:
        area_code = digits[0:3]
        exchange = digits[3:6]
        number = digits[6:10]
        return f"+1 ({area_code}) {exchange}-{number}"
    
    # If not parseable, return original
    else:
        return phone_str.strip()

for line in sys.stdin:
    if line.strip():
        print(format_phone_number(line))