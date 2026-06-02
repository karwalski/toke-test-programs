import sys
import re

def validate_branch_name(name):
    # Check for uppercase letters
    if re.search(r'[A-Z]', name):
        return False, "contains uppercase"
    
    # Check for spaces
    if ' ' in name:
        return False, "contains spaces"
    
    # Check for invalid characters (only allow alphanumeric, hyphens, underscores, and forward slashes)
    if not re.match(r'^[a-z0-9/_-]+$', name):
        return False, "contains invalid characters"
    
    # Check if it starts or ends with slash
    if name.startswith('/') or name.endswith('/'):
        return False, "starts or ends with slash"
    
    # Check for consecutive slashes
    if '//' in name:
        return False, "contains consecutive slashes"
    
    return True, ""

for line in sys.stdin:
    branch_name = line.strip()
    if branch_name:  # Skip empty lines
        is_valid, reason = validate_branch_name(branch_name)
        if is_valid:
            print(f"VALID: {branch_name}")
        else:
            print(f"INVALID: {branch_name} - {reason}")