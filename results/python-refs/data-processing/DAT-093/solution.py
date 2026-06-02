import sys
import re

def validate_email(email):
    email = email.strip()
    
    # Check if email contains exactly one @
    if email.count('@') != 1:
        if email.count('@') == 0:
            return False, "missing @ symbol"
        else:
            return False, "multiple @ symbols"
    
    # Split into local and domain parts
    local, domain = email.split('@', 1)
    
    # Check if local part is empty
    if not local:
        return False, "missing local part"
    
    # Check if domain part is empty
    if not domain:
        return False, "missing domain"
    
    # Validate local part
    if not validate_local_part(local):
        return False, "invalid local part"
    
    # Validate domain part
    if not validate_domain_part(domain):
        return False, "invalid domain"
    
    return True, ""

def validate_local_part(local):
    # Basic RFC 5322 local part validation
    if len(local) > 64:
        return False
    
    # Check for valid characters (simplified)
    # Allow alphanumeric, dot, hyphen, underscore, plus
    if not re.match(r'^[a-zA-Z0-9._+-]+$', local):
        return False
    
    # Cannot start or end with dot
    if local.startswith('.') or local.endswith('.'):
        return False
    
    # Cannot have consecutive dots
    if '..' in local:
        return False
    
    return True

def validate_domain_part(domain):
    # Basic RFC 5322 domain part validation
    if len(domain) > 253:
        return False
    
    # Domain cannot start or end with dot
    if domain.startswith('.') or domain.endswith('.'):
        return False
    
    # Split domain into labels
    labels = domain.split('.')
    
    # Must have at least one label
    if len(labels) < 1:
        return False
    
    # Each label must be valid
    for label in labels:
        if not label:  # Empty label (consecutive dots or leading/trailing dot)
            return False
        
        if len(label) > 63:
            return False
        
        # Label must start and end with alphanumeric
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', label):
            return False
    
    return True

def main():
    for line in sys.stdin:
        email = line.strip()
        if not email:
            continue
        
        is_valid, reason = validate_email(email)
        
        if is_valid:
            print(f"VALID {email}")
        else:
            print(f"INVALID {email}: {reason}")

if __name__ == "__main__":
    main()