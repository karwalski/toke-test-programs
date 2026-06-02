import re
import sys

def is_valid_email(email):
    # RFC 5322 simplified pattern
    # Local part: alphanumeric, dots, hyphens, underscores, plus signs
    # Domain part: alphanumeric, dots, hyphens, must have at least one dot
    pattern = r'^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False
    
    # Additional checks
    local_part, domain_part = email.rsplit('@', 1)
    
    # Local part cannot start or end with a dot
    if local_part.startswith('.') or local_part.endswith('.'):
        return False
    
    # Local part cannot have consecutive dots
    if '..' in local_part:
        return False
    
    # Domain part cannot start or end with a dot or hyphen
    if domain_part.startswith('.') or domain_part.endswith('.') or \
       domain_part.startswith('-') or domain_part.endswith('-'):
        return False
    
    # Domain part cannot have consecutive dots
    if '..' in domain_part:
        return False
    
    return True

for line in sys.stdin:
    email = line.strip()
    if email:
        if is_valid_email(email):
            print(f"{email}: VALID")
        else:
            print(f"{email}: INVALID")