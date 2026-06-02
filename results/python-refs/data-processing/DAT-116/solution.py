import sys
import re

def parse_currency(line):
    line = line.strip()
    
    # Handle different currency formats
    if line.startswith('$'):
        # US Dollar format: $1,234.56
        amount_str = line[1:].replace(',', '')
        return 'USD', float(amount_str)
    elif line.startswith('€'):
        # Euro format: €2.000,50 (European format with . as thousands separator and , as decimal)
        amount_str = line[1:]
        # Replace . with empty string (thousands separator) and , with . (decimal separator)
        amount_str = amount_str.replace('.', '').replace(',', '.')
        return 'EUR', float(amount_str)
    elif line.startswith('£'):
        # British Pound format: £99.99
        amount_str = line[1:].replace(',', '')
        return 'GBP', float(amount_str)
    elif line.startswith('JPY'):
        # Japanese Yen format: JPY 1500
        amount_str = line[4:].strip().replace(',', '')
        return 'JPY', float(amount_str)

def main():
    for line in sys.stdin:
        if line.strip():
            currency_code, amount = parse_currency(line)
            print(f"{currency_code} {amount:.2f}")

if __name__ == "__main__":
    main()