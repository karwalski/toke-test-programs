import os
import sys
from collections import defaultdict

def count_files_by_extension(directory):
    extension_counts = defaultdict(int)
    total_files = 0
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                total_files += 1
                # Get file extension (including the dot)
                _, ext = os.path.splitext(file)
                if ext == "":
                    ext = "(no extension)"
                extension_counts[ext] += 1
    except (OSError, PermissionError):
        # Handle cases where directory doesn't exist or no permission
        pass
    
    return extension_counts, total_files

def main():
    directory = input().strip()
    
    extension_counts, total_files = count_files_by_extension(directory)
    
    # Sort by count descending, then by extension name for ties
    sorted_extensions = sorted(extension_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Output extensions and counts
    for ext, count in sorted_extensions:
        print(f"{ext}: {count}")
    
    # Output total
    print(f"Total: {total_files} files.")

if __name__ == "__main__":
    main()