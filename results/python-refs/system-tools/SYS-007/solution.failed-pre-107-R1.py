import os
import shutil
import sys

def copy_directory():
    # Read input
    source = input().strip()
    destination = input().strip()
    
    copied = 0
    skipped = 0
    errors = 0
    
    # Create destination directory if it doesn't exist
    try:
        os.makedirs(destination, exist_ok=True)
    except:
        errors += 1
    
    # Walk through source directory
    if os.path.exists(source):
        for root, dirs, files in os.walk(source):
            # Calculate relative path
            rel_path = os.path.relpath(root, source)
            dest_dir = destination if rel_path == '.' else os.path.join(destination, rel_path)
            
            # Create destination subdirectories
            try:
                os.makedirs(dest_dir, exist_ok=True)
            except:
                errors += 1
                continue
            
            # Process files
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                
                try:
                    # Check if file needs to be copied
                    should_copy = True
                    
                    if os.path.exists(dest_file):
                        # Compare mtime and size
                        src_stat = os.stat(src_file)
                        dest_stat = os.stat(dest_file)
                        
                        if (src_stat.st_mtime == dest_stat.st_mtime and 
                            src_stat.st_size == dest_stat.st_size):
                            should_copy = False
                    
                    if should_copy:
                        shutil.copy2(src_file, dest_file)
                        copied += 1
                    else:
                        skipped += 1
                        
                except:
                    errors += 1
    
    # Print summary
    print(f"Copied: {copied} files")
    print(f"Skipped: {skipped} files")
    print(f"Errors: {errors} files")

copy_directory()