import sys
import os
from collections import defaultdict

def main():
    # Dictionary to store extension data: {ext: [count, total_size]}
    ext_data = defaultdict(lambda: [0, 0])
    
    # Read file paths from stdin
    for line in sys.stdin:
        filepath = line.strip()
        if not filepath:
            continue
            
        # Get file extension
        _, ext = os.path.splitext(filepath)
        ext = ext[1:] if ext.startswith('.') else ext  # Remove leading dot
        
        # If no extension, skip
        if not ext:
            continue
            
        # Get file size if file exists
        try:
            size = os.path.getsize(filepath)
        except (OSError, IOError):
            size = 0
            
        # Update counts and sizes
        ext_data[ext][0] += 1  # increment count
        ext_data[ext][1] += size  # add to total size
    
    # Sort by file count descending, then by extension name for ties
    sorted_exts = sorted(ext_data.items(), key=lambda x: (-x[1][0], x[0]))
    
    # Output results
    for ext, (count, total_size) in sorted_exts:
        size_kb = total_size // 1024  # Convert to KB
        print(f"{ext}: {count} files, {size_kb} KB")

if __name__ == "__main__":
    main()