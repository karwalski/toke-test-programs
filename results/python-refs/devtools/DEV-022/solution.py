import sys
import os
import re

def count_printable_strings(file_path, min_length=4):
    """Count printable strings in a binary file."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Find sequences of printable ASCII characters
        printable_pattern = rb'[ -~]{' + str(min_length).encode() + rb',}'
        strings = re.findall(printable_pattern, content)
        return len(strings)
    except:
        return 0

def get_file_type(file_path):
    """Determine basic file type based on file extension or name."""
    if os.path.isfile(file_path):
        return "file"
    else:
        return "unknown"

def main():
    # Read file path from stdin
    file_path = input().strip()
    
    # Get file type
    file_type = get_file_type(file_path)
    
    # Get file size
    try:
        size_bytes = os.path.getsize(file_path)
        size_kb = (size_bytes + 1023) // 1024  # Round up to nearest KB
    except:
        size_kb = 0
    
    # Count printable strings
    string_count = count_printable_strings(file_path)
    
    # Output in exact format
    print(f"{file_type}: {file_path}")
    print(f"size: {size_kb} KB")
    print(f"strings: {string_count}")

if __name__ == "__main__":
    main()