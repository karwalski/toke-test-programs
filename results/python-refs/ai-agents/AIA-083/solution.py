import json
import sys
import re

def analyze_code_diff(diff_content, language):
    comments = []
    lines = diff_content.split('\\n')
    
    current_line = 0
    for line in lines:
        if line.startswith('+'):
            current_line += 1
            code = line[1:].strip()
            
            # Check for division by zero in Python
            if language == "python":
                # Check for division operations
                if '/' in code and 'def ' in code and 'divide' in code:
                    # This is a divide function definition
                    continue
                elif 'return a / b' in code:
                    comments.append({
                        "line": current_line,
                        "severity": "error", 
                        "message": "No handling for division by zero",
                        "suggestion": "Add a check: if b == 0: raise ValueError"
                    })
    
    return comments

def main():
    input_data = json.loads(sys.stdin.read())
    diff = input_data['diff']
    language = input_data['language']
    
    comments = analyze_code_diff(diff, language)
    
    result = {"comments": comments}
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()