import sys

def strip_yaml_front_matter():
    lines = sys.stdin.read().splitlines()
    
    # Check if first line is YAML front matter delimiter
    if lines and lines[0].strip() == '---':
        # Find the closing delimiter
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                # Return everything after the closing delimiter
                body_lines = lines[i+1:]
                if body_lines:
                    print('\n'.join(body_lines))
                return
        
        # If no closing delimiter found, treat as regular markdown
        print('\n'.join(lines))
    else:
        # No front matter, return all content
        print('\n'.join(lines))

if __name__ == "__main__":
    strip_yaml_front_matter()