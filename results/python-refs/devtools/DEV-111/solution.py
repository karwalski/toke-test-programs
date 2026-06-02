import sys

def compress_log_lines():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        return
    
    current_line = lines[0]
    count = 1
    
    for i in range(1, len(lines)):
        # Extract the part after the date for comparison
        current_content = ' '.join(current_line.split()[1:]) if len(current_line.split()) > 1 else current_line
        next_content = ' '.join(lines[i].split()[1:]) if len(lines[i].split()) > 1 else lines[i]
        
        if current_content == next_content:
            count += 1
        else:
            # Output the current group
            if count > 1:
                print(f"{current_line} (repeated {count} times)")
            else:
                print(current_line)
            
            # Start new group
            current_line = lines[i]
            count = 1
    
    # Output the last group
    if count > 1:
        print(f"{current_line} (repeated {count} times)")
    else:
        print(current_line)

compress_log_lines()