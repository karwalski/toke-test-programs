import sys
import re

def validate_conventional_commit(message):
    # Pattern for conventional commit format
    # type(optional scope): description
    pattern = r'^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\([^)]+\))?: .+$'
    
    if re.match(pattern, message):
        return True, ""
    else:
        return False, "does not match conventional commit format"

def main():
    for line in sys.stdin:
        message = line.rstrip('\n')
        is_valid, reason = validate_conventional_commit(message)
        
        if is_valid:
            print(f"PASS: {message}")
        else:
            print(f"FAIL: {message} - {reason}")

if __name__ == "__main__":
    main()