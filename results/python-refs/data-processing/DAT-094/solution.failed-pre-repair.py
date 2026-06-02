import re
import sys

def parse_phone_number(phone_str):
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone_str.strip())
    
    # If it starts with +, it has a country code
    if cleaned.startswith('+'):
        # Already has country code, just return cleaned version
        if len(cleaned) >= 2:  # At least + and one digit
            return cleaned
        else:
            return 'INVALID'
    
    # If it doesn't start with +, check if it could be a US number
    if len(cleaned) == 10:
        # Assume US number, add +1
        return '+1' + cleaned
    elif len(cleaned) == 11 and cleaned.startswith('1'):
        # US number with 1 prefix
        return '+' + cleaned
    else:
        # No country code and not recognizable as US number
        return 'INVALID'

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        result = parse_phone_number(line)
        print(result)

if __name__ == "__main__":
    main()