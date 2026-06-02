import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except (IOError, OSError):
        return None

def find_duplicates(directory):
    """Find duplicate files in directory tree based on content hash."""
    hash_to_files = defaultdict(list)
    
    # Walk through directory tree
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    hash_to_files[file_hash].append(filepath)
    
    # Find groups with duplicates
    duplicate_groups = []
    for file_hash, files in hash_to_files.items():
        if len(files) > 1:
            # Sort to ensure consistent ordering
            files.sort()
            duplicate_groups.append(files)
    
    return duplicate_groups

def main():
    # Read input
    directory = input().strip()
    action = input().strip()
    
    # Check if directory exists
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print("No duplicates found")
        return
    
    # Find duplicates
    duplicate_groups = find_duplicates(directory)
    
    if not duplicate_groups:
        print("No duplicates found")
        return
    
    files_removed = 0
    
    # Process each group of duplicates
    for group in duplicate_groups:
        # First file is kept, rest are duplicates
        kept_file = group[0]
        duplicates = group[1:]
        
        for duplicate in duplicates:
            print(f"DUPLICATE {duplicate}")
            
            if action == "delete":
                try:
                    os.remove(duplicate)
                    files_removed += 1
                except (IOError, OSError):
                    pass
            elif action == "report":
                files_removed += 1
    
    # Print summary
    print(f"Summary: {len(duplicate_groups)} duplicate groups, {files_removed} files removed.")

if __name__ == "__main__":
    main()