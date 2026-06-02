import sys
import re
import json

def main():
    lines = sys.stdin.read().strip().split('\n')
    pattern_template = lines[0]
    log_lines = lines[1:]
    
    # Convert template to regex pattern
    # Replace {name} with named capture groups
    regex_pattern = pattern_template
    placeholders = re.findall(r'\{(\w+)\}', pattern_template)
    
    for placeholder in placeholders:
        regex_pattern = regex_pattern.replace(f'{{{placeholder}}}', f'(?P<{placeholder}>\\S+)')
    
    # Handle remaining spaces as whitespace matches
    regex_pattern = regex_pattern.replace(' ', r'\s+')
    
    # For the message field, we need to capture everything to the end
    if 'message' in placeholders:
        regex_pattern = regex_pattern.replace(f'(?P<message>\\S+)', f'(?P<message>.*)')
    
    compiled_pattern = re.compile(regex_pattern)
    
    for log_line in log_lines:
        match = compiled_pattern.match(log_line)
        if match:
            result = match.groupdict()
            print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()