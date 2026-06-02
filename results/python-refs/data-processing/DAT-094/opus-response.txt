import re
import sys

def parse_phone_number(phone_str):
    cleaned = re.sub(r'[^\d+]', '', phone_str.strip())
    
    if cleaned.startswith('+'):
        if len(cleaned) >= 2:
            return cleaned
        else:
            return 'INVALID'
    
    if len(cleaned) == 10:
        return '+1' + cleaned
    elif len(cleaned) == 11 and cleaned.startswith('1'):
        return '+' + cleaned
    else:
        return 'INVALID (no country code)'

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        print(parse_phone_number(line))

if __name__ == "__main__":
    main()