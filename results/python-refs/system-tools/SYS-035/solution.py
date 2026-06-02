import os
import sys

def get_size_str(size):
    """Convert size in bytes to human readable string"""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size // 1024}K"
    elif size < 1024 * 1024 * 1024:
        return f"{size // (1024 * 1024)}M"
    else:
        return f"{size // (1024 * 1024 * 1024)}G"

def print_tree(path, max_depth, current_depth=0, prefix="", is_last=True):
    """Print directory tree recursively"""
    dir_count = 0
    file_count = 0
    
    if not os.path.exists(path):
        return dir_count, file_count
    
    if current_depth == 0:
        print(os.path.basename(path) if os.path.basename(path) else path)
    
    if max_depth > 0 and current_depth >= max_depth:
        return dir_count, file_count
    
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return dir_count, file_count
    
    for i, entry in enumerate(entries):
        entry_path = os.path.join(path, entry)
        is_last_entry = (i == len(entries) - 1)
        
        if current_depth == 0:
            connector = "└── " if is_last_entry else "├── "
            new_prefix = "    " if is_last_entry else "│   "
        else:
            connector = prefix + ("└── " if is_last_entry else "├── ")
            new_prefix = prefix + ("    " if is_last_entry else "│   ")
        
        if os.path.isdir(entry_path):
            print(f"{connector}{entry}/")
            dir_count += 1
            sub_dirs, sub_files = print_tree(entry_path, max_depth, current_depth + 1, new_prefix, is_last_entry)
            dir_count += sub_dirs
            file_count += sub_files
        else:
            try:
                size = os.path.getsize(entry_path)
                size_str = get_size_str(size)
                print(f"{connector}{entry} [{size_str}]")
            except (OSError, PermissionError):
                print(f"{connector}{entry}")
            file_count += 1
    
    return dir_count, file_count

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    directory_path = lines[0]
    max_depth = int(lines[1])
    
    dir_count, file_count = print_tree(directory_path, max_depth)
    
    print(f"\n{dir_count} directories, {file_count} files")

if __name__ == "__main__":
    main()