import os
import sys

def format_size(size_bytes):
    return f"{size_bytes} B"

def main():
    files = []
    total_size = 0
    
    # Read file paths from stdin
    for line in sys.stdin:
        file_path = line.strip()
        if file_path:
            try:
                size = os.path.getsize(file_path)
                files.append((size, file_path))
                total_size += size
            except (OSError, FileNotFoundError):
                # If file doesn't exist or can't be accessed, treat as 0 size
                files.append((0, file_path))
    
    # Sort by size descending
    files.sort(key=lambda x: x[0], reverse=True)
    
    # Output files with sizes
    for size, file_path in files:
        print(f"{file_path}: {format_size(size)}")
    
    # Output total
    print(f"Total: {format_size(total_size)}")

if __name__ == "__main__":
    main()