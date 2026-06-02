import json
import sys
import string

def validate_password(password, policy):
    violations = []
    
    # Check minimum length
    if "minLength" in policy and len(password) < policy["minLength"]:
        violations.append(f"minimum length {policy['minLength']}")
    
    # Check uppercase requirement
    if policy.get("requireUpper", False):
        if not any(c.isupper() for c in password):
            violations.append("uppercase letter")
    
    # Check lowercase requirement
    if policy.get("requireLower", False):
        if not any(c.islower() for c in password):
            violations.append("lowercase letter")
    
    # Check digit requirement
    if policy.get("requireDigit", False):
        if not any(c.isdigit() for c in password):
            violations.append("digit")
    
    # Check special character requirement
    if policy.get("requireSpecial", False):
        special_chars = set(string.punctuation)
        if not any(c in special_chars for c in password):
            violations.append("special character")
    
    return violations

def main():
    # Read policy from first line
    policy_line = input().strip()
    policy = json.loads(policy_line)
    
    # Read passwords until blank line
    while True:
        try:
            password = input()
            if password == "":
                break
            
            violations = validate_password(password, policy)
            
            if not violations:
                print("PASS")
            else:
                print("FAIL")
                for violation in violations:
                    print(f"- Missing: {violation}")
        except EOFError:
            break

if __name__ == "__main__":
    main()