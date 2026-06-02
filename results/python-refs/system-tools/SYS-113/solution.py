import os
import hashlib

def compute_file_hash(filepath):
    """Compute SHA-256 hash of a file's contents."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError):
        # If file can't be read, return empty string hash
        return hashlib.sha256(b"").hexdigest()

def compute_directory_hash(directory_path):
    """Compute a hash representing the entire directory tree."""
    file_hashes = []
    
    try:
        # Walk through all files in the directory tree
        for root, dirs, files in os.walk(directory_path):
            # Sort directories and files for consistent ordering
            dirs.sort()
            files.sort()
            
            for filename in files:
                filepath = os.path.join(root, filename)
                # Create a string that includes both the relative path and file hash
                relative_path = os.path.relpath(filepath, directory_path)
                file_hash = compute_file_hash(filepath)
                # Combine path and hash for uniqueness
                combined = f"{relative_path}:{file_hash}"
                file_hashes.append(combined)
    except (IOError, OSError):
        # If directory can't be accessed, treat as empty
        pass
    
    # Sort all file entries for consistent ordering
    file_hashes.sort()
    
    # Create final hash from all sorted file hashes
    final_hasher = hashlib.sha256()
    for entry in file_hashes:
        final_hasher.update(entry.encode('utf-8'))
    
    return final_hasher.hexdigest()

# Read input
directory_path = input().strip()

# Compute and output the directory hash
directory_hash = compute_directory_hash(directory_path)
print(f"Directory hash: {directory_hash}")