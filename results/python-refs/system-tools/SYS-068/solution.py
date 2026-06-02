import sys

def main():
    lines = sys.stdin.read().strip().split('\n')
    options_line = lines[0]
    data_lines = lines[1:]
    
    # Parse options
    options = [opt.strip() for opt in options_line.split(',')]
    
    numeric = 'numeric' in options
    reverse = 'reverse' in options
    ignore_case = 'ignore-case' in options
    field_num = None
    
    for opt in options:
        if opt.startswith('field='):
            field_num = int(opt.split('=')[1]) - 1  # Convert to 0-based index
    
    # Define sort key function
    def sort_key(line):
        if field_num is not None:
            fields = line.split()
            if field_num < len(fields):
                value = fields[field_num]
            else:
                value = ""
        else:
            value = line
        
        if ignore_case:
            value = value.lower()
        
        if numeric:
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    return 0
        
        return value
    
    # Sort the lines
    sorted_lines = sorted(data_lines, key=sort_key, reverse=reverse)
    
    # Output
    for line in sorted_lines:
        print(line)

if __name__ == "__main__":
    main()