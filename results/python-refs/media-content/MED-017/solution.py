import sys
import re

def validate_markdown_headings():
    lines = sys.stdin.read().strip().split('\n')
    violations = []
    current_level = 0
    
    for i, line in enumerate(lines, 1):
        # Check if line is a heading
        match = re.match(r'^(#+)\s', line)
        if match:
            level = len(match.group(1))
            
            # Check if we're skipping levels
            if level > current_level + 1:
                violations.append(f"Line {i}: Heading level {level} skips from level {current_level}")
            
            current_level = level
    
    if violations:
        for violation in violations:
            print(violation)
    else:
        print("PASS")

validate_markdown_headings()