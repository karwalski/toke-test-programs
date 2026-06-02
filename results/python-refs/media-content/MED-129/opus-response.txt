import sys
import re

def main():
    text = sys.stdin.read().strip()
    lines = text.split('\n')
    result = []
    i = 0
    current_type = None
    current_content = []
    
    def flush():
        if current_type is not None:
            result.append(f'```{current_type}')
            result.extend(current_content)
            result.append('```')
    
    while i < len(lines):
        line = lines[i]
        match = re.match(r'^(NOTE|WARNING|TIP|INFO):\s*(.*)', line)
        if match:
            flush()
            current_type = match.group(1).lower()
            current_content = [match.group(2)]
        elif current_type is not None and line.strip():
            current_content.append(line)
        else:
            flush()
            current_type = None
            current_content = []
            result.append(line)
        i += 1
    
    flush()
    if current_type is None and not result:
        pass
    
    # Remove trailing empty result entries that came from non-admonition handling
    output = '\n'.join(result)
    print(output)

main()