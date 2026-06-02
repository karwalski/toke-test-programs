import sys

def estimate_python_memory(line):
    line = line.strip()
    
    # List allocation patterns
    if '[' in line and ']' in line and '*' in line:
        # Pattern: [value] * count
        try:
            # Extract the multiplication part
            if ' * ' in line:
                parts = line.split(' * ')
                if len(parts) >= 2:
                    count_part = parts[1].split(']')[0]
                    count = int(count_part)
                    
                    # Estimate 8 bytes per integer element
                    bytes_total = count * 8
                    
                    if bytes_total >= 1000000:
                        mb = bytes_total / 1000000
                        return f"  # ~{int(mb)}MB"
        except:
            pass
    
    return ""

def process_line(line, language):
    if language == "python":
        annotation = estimate_python_memory(line)
        return line.rstrip() + annotation
    return line.rstrip()

# Read input
lines = sys.stdin.read().strip().split('\n')
language = lines[0].strip()

# Process source lines
for i in range(1, len(lines)):
    result = process_line(lines[i], language)
    print(result)