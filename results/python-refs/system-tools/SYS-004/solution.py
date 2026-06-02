import os
import sys

def get_size(path):
    """Get total size of directory and all its contents"""
    total = 0
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total += os.path.getsize(filepath)
                except (OSError, IOError):
                    pass
    except (OSError, IOError):
        pass
    return total

def format_size(size):
    """Convert size in bytes to human readable format"""
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024.0:
            if unit == 'B':
                return f"{size:.0f}{unit}"
            else:
                return f"{size:.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}P"

def main():
    # Read input
    directory_path = input().strip()
    n = int(input().strip())
    
    # Get all subdirectories
    subdirs = []
    try:
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                size = get_size(item_path)
                subdirs.append((size, item_path))
    except (OSError, IOError):
        pass
    
    # Sort by size descending
    subdirs.sort(key=lambda x: x[0], reverse=True)
    
    # Show top N
    total_size = 0
    for i, (size, path) in enumerate(subdirs[:n]):
        print(f"{format_size(size)} {path}")
        total_size += size
    
    # Add remaining subdirectories to total
    for size, path in subdirs[n:]:
        total_size += size
    
    # Also add files in the root directory
    try:
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                try:
                    total_size += os.path.getsize(item_path)
                except (OSError, IOError):
                    pass
    except (OSError, IOError):
        pass
    
    # Print total
    print(f"{format_size(total_size)} total")

if __name__ == "__main__":
    main()