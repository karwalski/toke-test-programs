import sys

def format_outline():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    counters = [0, 0, 0]  # counters for levels 0, 1, 2
    markers = ['I', 'A', '1']
    
    for line in lines:
        if not line.strip():
            continue
            
        # Count leading spaces to determine level
        indent = 0
        for char in line:
            if char == ' ':
                indent += 1
            else:
                break
        
        level = indent // 2
        content = line.strip()
        
        # Reset counters for deeper levels when we're at a higher level
        for i in range(level + 1, 3):
            counters[i] = 0
        
        # Increment counter for current level
        counters[level] += 1
        
        # Format the marker
        if level == 0:
            marker = f"{counters[level]}."
            # Convert to Roman numeral
            roman_numerals = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
            if counters[level] <= len(roman_numerals):
                marker = f"{roman_numerals[counters[level] - 1]}."
        elif level == 1:
            # Convert to letter
            letter = chr(ord('A') + counters[level] - 1)
            marker = f"{letter}."
        else:  # level == 2
            marker = f"{counters[level]}."
        
        # Output with proper indentation
        output_indent = '  ' * level
        print(f"{output_indent}{marker} {content}")

format_outline()