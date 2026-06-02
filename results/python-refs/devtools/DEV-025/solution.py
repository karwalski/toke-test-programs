import sys
import re

def parse_stack_trace():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    print("Stack trace:")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines and goroutine headers
        if not line or line.startswith('goroutine'):
            i += 1
            continue
            
        # Check if this is a function call line (doesn't start with whitespace in original)
        if not lines[i].startswith('\t') and not lines[i].startswith(' '):
            func_name = line
            # Look for the next line which should contain file info
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Parse file path and line number
                match = re.match(r'(.+):(\d+)', next_line.split()[0])
                if match:
                    file_path = match.group(1)
                    line_num = match.group(2)
                    print(f"  {func_name} at {file_path}:{line_num}")
                i += 2
            else:
                i += 1
        else:
            i += 1

if __name__ == "__main__":
    parse_stack_trace()