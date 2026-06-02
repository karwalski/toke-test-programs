import os
import hashlib
import json
import sys
from datetime import datetime

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

def create_snapshot(directory):
    """Create a snapshot of all files in directory and subdirectories."""
    snapshot = {}
    file_count = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_file_hash(filepath)
            if file_hash is not None:
                # Store relative path from the watched directory
                rel_path = os.path.relpath(filepath, directory)
                snapshot[rel_path] = file_hash
                file_count += 1
    
    return snapshot, file_count

def save_snapshot(snapshot, directory):
    """Save snapshot to a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_file = f"snapshot_{timestamp}.json"
    
    with open(snapshot_file, 'w') as f:
        json.dump(snapshot, f, indent=2)
    
    return snapshot_file

def load_snapshot(snapshot_file):
    """Load snapshot from a file."""
    try:
        with open(snapshot_file, 'r') as f:
            return json.load(f)
    except (IOError, FileNotFoundError):
        return {}

def compare_snapshots(old_snapshot, new_snapshot):
    """Compare two snapshots and return changes."""
    changes = []
    
    # Find added and modified files
    for filepath, new_hash in new_snapshot.items():
        if filepath not in old_snapshot:
            changes.append(f"ADDED {filepath}")
        elif old_snapshot[filepath] != new_hash:
            changes.append(f"MODIFIED {filepath}")
    
    # Find deleted files
    for filepath in old_snapshot:
        if filepath not in new_snapshot:
            changes.append(f"DELETED {filepath}")
    
    return sorted(changes)

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    directory = lines[0]
    command = lines[1]
    
    if command == "snapshot":
        snapshot, file_count = create_snapshot(directory)
        snapshot_file = save_snapshot(snapshot, directory)
        print(f"Snapshot saved to {snapshot_file} ({file_count} files)")
    
    elif command == "diff":
        previous_snapshot_file = lines[2]
        
        # Load previous snapshot
        old_snapshot = load_snapshot(previous_snapshot_file)
        
        # Create current snapshot
        new_snapshot, _ = create_snapshot(directory)
        
        # Compare snapshots
        changes = compare_snapshots(old_snapshot, new_snapshot)
        
        # Output changes
        for change in changes:
            print(change)

if __name__ == "__main__":
    main()