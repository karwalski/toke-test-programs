import os
import json
import hashlib
import sys

def compute_sha256(filepath):
    """Compute SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except (IOError, OSError):
        return None

def get_all_files(directory):
    """Get all files in directory and subdirectories with their hashes."""
    file_hashes = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == '.fim-baseline.json':
                continue
            filepath = os.path.join(root, file)
            # Use relative path from the directory
            relative_path = os.path.relpath(filepath, directory)
            file_hash = compute_sha256(filepath)
            if file_hash is not None:
                file_hashes[relative_path] = file_hash
    
    return file_hashes

def save_baseline(directory, file_hashes):
    """Save baseline hashes to .fim-baseline.json."""
    baseline_path = os.path.join(directory, '.fim-baseline.json')
    try:
        with open(baseline_path, 'w') as f:
            json.dump(file_hashes, f, indent=2, sort_keys=True)
        return True
    except (IOError, OSError):
        return False

def load_baseline(directory):
    """Load baseline hashes from .fim-baseline.json."""
    baseline_path = os.path.join(directory, '.fim-baseline.json')
    try:
        with open(baseline_path, 'r') as f:
            return json.load(f)
    except (IOError, OSError, json.JSONDecodeError):
        return None

def compare_hashes(baseline, current):
    """Compare baseline and current hashes, return changes."""
    changes = []
    
    # Find added and modified files
    for filepath, current_hash in current.items():
        if filepath not in baseline:
            changes.append(f"ADDED {filepath}")
        elif baseline[filepath] != current_hash:
            changes.append(f"MODIFIED {filepath}")
    
    # Find deleted files
    for filepath in baseline:
        if filepath not in current:
            changes.append(f"DELETED {filepath}")
    
    return sorted(changes)

def main():
    # Read input
    directory = input().strip()
    mode = input().strip()
    
    if not os.path.isdir(directory):
        print(f"Error: Directory {directory} does not exist")
        return
    
    if mode == "baseline":
        # Create baseline
        file_hashes = get_all_files(directory)
        if save_baseline(directory, file_hashes):
            print("Baseline saved")
        else:
            print("Error: Could not save baseline")
    
    elif mode == "check":
        # Check against baseline
        baseline = load_baseline(directory)
        if baseline is None:
            print("Error: No baseline found")
            return
        
        current = get_all_files(directory)
        changes = compare_hashes(baseline, current)
        
        for change in changes:
            print(change)
    
    else:
        print(f"Error: Invalid mode {mode}")

if __name__ == "__main__":
    main()