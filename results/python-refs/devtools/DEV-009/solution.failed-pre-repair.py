import json
import re
import sys

def main():
    # Read all input
    lines = sys.stdin.read().strip().split('\n')
    
    # First line contains the JSON rules array
    rules_json = lines[0]
    rules = json.loads(rules_json)
    
    # Remaining lines are the source code
    source_lines = lines[1:] if len(lines) > 1 else []
    
    # Check each line of source code against each rule
    violations = []
    
    for line_num, line in enumerate(source_lines, 1):
        for rule in rules:
            rule_id = rule['id']
            pattern = rule['pattern']
            message = rule['message']
            severity = rule['severity']
            
            # Check if the pattern matches the line
            if re.search(pattern, line):
                violation = f"line {line_num}: [{severity}] {rule_id} - {message}"
                violations.append(violation)
    
    # Output violations
    for violation in violations:
        print(violation)

if __name__ == "__main__":
    main()