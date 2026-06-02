import os
import shutil
from pathlib import Path

def get_file_info(filepath):
    """Get file modification time and size"""
    stat = os.stat(filepath)
    return (stat.st_mtime, stat.st_size)

def should_copy(src_file, dst_file):
    """Check if source file should be copied to destination"""
    if not os.path.exists(dst_file):
        return True
    
    src_info = get_file_info(src_file)
    dst_info = get_file_info(dst_file)
    
    # Copy if source is newer or different size
    return src_info[0] > dst_info[0] or src_info[1] != dst_info[1]

def sync_directories():
    # Read input
    source_path = input().strip()
    dest_path = input().strip()
    delete_option = input().strip().lower() == 'yes'
    
    copied = 0
    skipped = 0
    deleted = 0
    
    # Create destination directory if it doesn't exist
    os.makedirs(dest_path, exist_ok=True)
    
    # Get all files in source directory recursively
    source_files = set()
    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), source_path)
                source_files.add(rel_path)
                
                src_file = os.path.join(source_path, rel_path)
                dst_file = os.path.join(dest_path, rel_path)
                
                # Create destination directory if needed
                dst_dir = os.path.dirname(dst_file)
                if dst_dir:
                    os.makedirs(dst_dir, exist_ok=True)
                
                if should_copy(src_file, dst_file):
                    shutil.copy2(src_file, dst_file)
                    print(f"COPY {rel_path}")
                    copied += 1
                else:
                    print(f"SKIP {rel_path}")
                    skipped += 1
    
    # Handle deletion if requested
    if delete_option and os.path.exists(dest_path):
        for root, dirs, files in os.walk(dest_path):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), dest_path)
                if rel_path not in source_files:
                    dst_file = os.path.join(dest_path, rel_path)
                    os.remove(dst_file)
                    print(f"DELETE {rel_path}")
                    deleted += 1
    
    print(f"Done: {copied} copied, {skipped} skipped, {deleted} deleted")

sync_directories()