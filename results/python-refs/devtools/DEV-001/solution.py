import sys
import os
from collections import defaultdict

def count_lines_in_file(filepath):
    """Count code, comment, and blank lines in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except:
        return 0, 0, 0
    
    code_lines = 0
    comment_lines = 0
    blank_lines = 0
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank_lines += 1
        elif stripped.startswith('#'):
            comment_lines += 1
        else:
            code_lines += 1
    
    return code_lines, comment_lines, blank_lines

def main():
    stats = defaultdict(lambda: {'files': 0, 'code': 0, 'comment': 0, 'blank': 0})
    
    for line in sys.stdin:
        filepath = line.strip()
        if not filepath:
            continue
            
        if os.path.isfile(filepath):
            _, ext = os.path.splitext(filepath)
            if not ext:
                ext = '(no extension)'
            
            code, comment, blank = count_lines_in_file(filepath)
            
            stats[ext]['files'] += 1
            stats[ext]['code'] += code
            stats[ext]['comment'] += comment
            stats[ext]['blank'] += blank
    
    # Print header
    print("ext    | files | code | comment | blank | total")
    
    # Print stats for each extension
    for ext in sorted(stats.keys()):
        s = stats[ext]
        total = s['code'] + s['comment'] + s['blank']
        print(f"{ext:<6} | {s['files']:5} | {s['code']:4} | {s['comment']:7} | {s['blank']:5} | {total:5}")

if __name__ == "__main__":
    main()