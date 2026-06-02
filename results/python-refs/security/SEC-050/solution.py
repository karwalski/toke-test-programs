import sys
import json
import re

def scan_prototype_pollution(code_lines):
    vulnerabilities = []
    
    for line_num, line in enumerate(code_lines, 1):
        line = line.strip()
        if not line:
            continue
            
        # Check for merge/extend function patterns that could allow prototype pollution
        if is_vulnerable_merge_extend(line):
            vulnerabilities.append({
                "line": line_num,
                "code_snippet": line,
                "vulnerability": "prototype_pollution",
                "severity": "high",
                "recommendation": "Add checks to prevent __proto__, constructor, and prototype key assignments"
            })
    
    return vulnerabilities

def is_vulnerable_merge_extend(line):
    # Look for function definitions with merge/extend-like patterns
    function_patterns = [
        r'function\s+(merge|extend)\s*\(',
        r'(merge|extend)\s*[:=]\s*function',
        r'(merge|extend)\s*=\s*\(',
    ]
    
    for pattern in function_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    
    # Look for vulnerable assignment patterns in loops
    assignment_patterns = [
        r'target\s*\[\s*key\s*\]\s*=\s*source\s*\[\s*key\s*\]',
        r'obj\s*\[\s*key\s*\]\s*=\s*.*\[\s*key\s*\]',
        r'\w+\s*\[\s*\w+\s*\]\s*=\s*\w+\s*\[\s*\w+\s*\]',
    ]
    
    # Check if this line contains a vulnerable assignment pattern
    # and is likely part of a merge/extend function
    for pattern in assignment_patterns:
        if re.search(pattern, line):
            # Check if it's in a for-in loop context (simple heuristic)
            if 'for' in line or 'target' in line or 'source' in line:
                return True
    
    return False

def main():
    code_lines = []
    for line in sys.stdin:
        code_lines.append(line.rstrip('\n'))
    
    vulnerabilities = scan_prototype_pollution(code_lines)
    
    if vulnerabilities:
        print("prototype_pollution")

if __name__ == "__main__":
    main()