import re
import os
import sys

def search_files(pattern, path, recursive):
    regex = re.compile(pattern)
    
    if os.path.isfile(path):
        # Single file
        search_in_file(regex, path)
    elif os.path.isdir(path):
        # Directory
        if recursive:
            for root, dirs, files in os.walk(path):
                for file in files:
                    filepath = os.path.join(root, file)
                    search_in_file(regex, filepath)
        else:
            try:
                for item in os.listdir(path):
                    filepath = os.path.join(path, item)
                    if os.path.isfile(filepath):
                        search_in_file(regex, filepath)
            except (PermissionError, OSError):
                pass

def search_in_file(regex, filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n\r')
                if regex.search(line):
                    print(f"{filepath}:{line_num}:{line}")
    except (PermissionError, OSError, UnicodeDecodeError):
        pass

# Read input
pattern = input().strip()
path = input().strip()
recursive_input = input().strip().lower()
recursive = recursive_input == 'yes'

# Search files
search_files(pattern, path, recursive)