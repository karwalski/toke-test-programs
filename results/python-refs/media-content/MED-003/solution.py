import sys
import re

def generate_anchor(text):
    # Convert to lowercase and replace spaces/special chars with hyphens
    anchor = re.sub(r'[^\w\s-]', '', text.lower())
    anchor = re.sub(r'[\s_-]+', '-', anchor)
    anchor = anchor.strip('-')
    return anchor

def main():
    lines = sys.stdin.read().strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # Count the number of # characters to determine heading level
            level = 0
            for char in line:
                if char == '#':
                    level += 1
                else:
                    break
            
            # Extract heading text (remove # and leading/trailing spaces)
            heading_text = line[level:].strip()
            
            # Generate anchor link
            anchor = generate_anchor(heading_text)
            
            # Create indentation based on level (2 spaces per level after first)
            indent = '  ' * (level - 1)
            
            # Output the TOC entry
            print(f"{indent}- [{heading_text}](#{anchor})")

if __name__ == "__main__":
    main()