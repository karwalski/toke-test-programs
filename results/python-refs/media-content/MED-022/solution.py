import sys

def main():
    # Read all input
    content = sys.stdin.read()
    
    # Split by the separator line
    parts = content.split('\n---\n')
    if len(parts) != 2:
        return
    
    # Get the two text blocks
    text1_lines = parts[0].split('\n')
    text2_lines = parts[1].rstrip('\n').split('\n')
    
    # Simple line-by-line diff
    max_lines = max(len(text1_lines), len(text2_lines))
    
    i = 0
    j = 0
    
    while i < len(text1_lines) or j < len(text2_lines):
        if i < len(text1_lines) and j < len(text2_lines):
            if text1_lines[i] == text2_lines[j]:
                # Same line
                print(' ' + text1_lines[i])
                i += 1
                j += 1
            else:
                # Different lines - treat as remove and add
                print('-' + text1_lines[i])
                print('+' + text2_lines[j])
                i += 1
                j += 1
        elif i < len(text1_lines):
            # Only text1 has remaining lines (removals)
            print('-' + text1_lines[i])
            i += 1
        else:
            # Only text2 has remaining lines (additions)
            print('+' + text2_lines[j])
            j += 1

if __name__ == '__main__':
    main()