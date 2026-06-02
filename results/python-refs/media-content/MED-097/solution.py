import re
import sys

def mask_credit_card(text):
    # Pattern to match credit card numbers with dashes
    pattern = r'\b(\d{4})-(\d{4})-(\d{4})-(\d{4})\b'
    
    def replace_func(match):
        last_four = match.group(4)
        return f'XXXX-XXXX-XXXX-{last_four}'
    
    return re.sub(pattern, replace_func, text)

# Read from stdin and process
for line in sys.stdin:
    print(mask_credit_card(line.rstrip('\n')))