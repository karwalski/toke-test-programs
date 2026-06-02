import os
import sys
import time
import fnmatch
from pathlib import Path

def main():
    # Read input
    lines = [line.strip() for line in sys.stdin.readlines()]
    
    if not lines:
        return
    
    root_dir = lines[0]
    
    # Parse criteria
    name_pattern = None
    size_min = None
    size_max = None
    mtime_days = None
    
    for line in lines[1:]:
        if line.startswith("name "):
            name_pattern = line[5:]
        elif line.startswith("size_min "):
            size_min = int(line[9:])
        elif line.startswith("size_max "):
            size_max = int(line[9:])
        elif line.startswith("mtime_days "):
            mtime_days = int(line[11:])
    
    # Find matching files
    matching_files = []
    current_time = time.time()
    
    try:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    # Check if file exists and get stats
                    stat_info = os.stat(file_path)
                    
                    # Check name pattern
                    if name_pattern and not fnmatch.fnmatch(file, name_pattern):
                        continue
                    
                    # Check size constraints
                    file_size = stat_info.st_size
                    if size_min is not None and file_size < size_min:
                        continue
                    if size_max is not None and file_size > size_max:
                        continue
                    
                    # Check modification time
                    if mtime_days is not None:
                        file_mtime = stat_info.st_mtime
                        days_ago = (current_time - file_mtime) / (24 * 3600)
                        if days_ago > mtime_days:
                            continue
                    
                    matching_files.append(file_path)
                
                except (OSError, IOError):
                    # Skip files we can't access
                    continue
    
    except (OSError, IOError):
        # Skip directories we can't access
        pass
    
    # Output results
    for file_path in sorted(matching_files):
        print(file_path)
    
    print(f"{len(matching_files)} files found.")

if __name__ == "__main__":
    main()