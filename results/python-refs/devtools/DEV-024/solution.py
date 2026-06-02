import sys
import re
from collections import defaultdict

def main():
    errors = defaultdict(list)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        # Parse format: file:line:col: error: message
        match = re.match(r'^([^:]+):(\d+):(\d+):\s*error:\s*(.+)$', line)
        if match:
            filename, line_num, col_num, message = match.groups()
            errors[filename].append((int(line_num), int(col_num), message))
    
    # Sort files by name for consistent output
    for filename in sorted(errors.keys()):
        error_list = errors[filename]
        count = len(error_list)
        error_word = "error" if count == 1 else "errors"
        print(f"{filename} ({count} {error_word})")
        
        # Sort errors by line number, then column number
        error_list.sort()
        
        for line_num, col_num, message in error_list:
            print(f"  line {line_num}, col {col_num}: {message}")

if __name__ == "__main__":
    main()