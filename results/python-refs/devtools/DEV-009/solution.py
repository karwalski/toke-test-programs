import json
import re
import sys

def main():
    data = sys.stdin.read()
    # The first line is JSON. But JSON may contain escaped chars; split on first newline.
    # However the issue is that json.loads on the first line may fail if the JSON contains
    # actual newlines or if escape sequences are interpreted. Try parsing incrementally.
    
    decoder = json.JSONDecoder()
    # Skip leading whitespace
    idx = 0
    while idx < len(data) and data[idx] in ' \t':
        idx += 1
    
    try:
        rules, end = decoder.raw_decode(data, idx)
    except json.JSONDecodeError:
        # Fallback: try first line
        if '\n' in data:
            first_line, rest = data.split('\n', 1)
        else:
            first_line, rest = data, ''
        rules = json.loads(first_line)
        end = len(first_line) + 1 if '\n' in data else len(first_line)
    
    rest = data[end:]
    # Skip one newline after JSON
    if rest.startswith('\n'):
        rest = rest[1:]
    elif rest.startswith('\r\n'):
        rest = rest[2:]
    
    source_lines = rest.split('\n') if rest else []
    
    violations = []
    
    for line_num, line in enumerate(source_lines, 1):
        line_violations = []
        for rule in rules:
            rule_id = rule['id']
            pattern = rule['pattern']
            message = rule['message']
            severity = rule['severity']
            
            if re.search(pattern, line):
                line_violations.append((line_num, rule_id, severity, message))
        
        line_violations.sort(key=lambda x: (x[0], x[1]))
        violations.extend(line_violations)
    
    for ln, rid, sev, msg in violations:
        print(f"line {ln}: [{sev}] {rid} - {msg}")

if __name__ == "__main__":
    main()