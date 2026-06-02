import os
import glob
import shutil
import sys

def move_files():
    # Read input
    source_dir = input().strip()
    dest_dir = input().strip()
    pattern = input().strip()
    conflict_mode = input().strip()
    
    moved_count = 0
    skipped_count = 0
    error_count = 0
    
    # Create destination directory if it doesn't exist
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except Exception:
        error_count += 1
        print(f"Summary: {moved_count} files moved, {skipped_count} skipped, {error_count} errors.")
        return
    
    # Get full pattern path
    full_pattern = os.path.join(source_dir, pattern)
    
    # Find matching files
    try:
        matching_files = glob.glob(full_pattern)
        matching_files = [f for f in matching_files if os.path.isfile(f)]
    except Exception:
        matching_files = []
    
    for src_file in matching_files:
        try:
            filename = os.path.basename(src_file)
            dst_file = os.path.join(dest_dir, filename)
            
            # Check if destination file exists
            if os.path.exists(dst_file):
                if conflict_mode == "skip":
                    skipped_count += 1
                    continue
                elif conflict_mode == "overwrite":
                    pass  # Will overwrite
                elif conflict_mode == "rename":
                    # Find a new name
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(dst_file):
                        new_filename = f"{base}_{counter}{ext}"
                        dst_file = os.path.join(dest_dir, new_filename)
                        counter += 1
            
            # Move the file
            shutil.move(src_file, dst_file)
            print(f"MOVED {src_file} -> {dst_file}")
            moved_count += 1
            
        except Exception:
            error_count += 1
    
    print(f"Summary: {moved_count} files moved, {skipped_count} skipped, {error_count} errors.")

if __name__ == "__main__":
    move_files()