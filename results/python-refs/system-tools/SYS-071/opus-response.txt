import os
import hashlib
import json
import sys

def calculate_file_hash(filepath):
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except (IOError, OSError):
        return None

def get_file_size(filepath):
    try:
        return os.path.getsize(filepath)
    except (IOError, OSError):
        return None

def get_file_mtime(filepath):
    try:
        return os.path.getmtime(filepath)
    except (IOError, OSError):
        return None

def build_manifest(directory):
    manifest = {}
    file_count = 0
    
    if not os.path.exists(directory):
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError:
            pass
    
    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == '.manifest.json':
                    continue
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, directory)
                
                file_hash = calculate_file_hash(filepath)
                file_size = get_file_size(filepath)
                file_mtime = get_file_mtime(filepath)
                
                if file_hash is not None and file_size is not None:
                    manifest[relative_path] = {
                        'hash': file_hash,
                        'size': file_size,
                        'mtime': file_mtime
                    }
                    file_count += 1
    
    manifest_path = '/tmp/manifest.json'
    try:
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
    except OSError:
        manifest_path = os.path.join(os.getcwd(), 'manifest.json')
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
    
    return manifest_path, file_count

def check_manifest(directory, manifest_path):
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except (IOError, OSError, json.JSONDecodeError):
        manifest = {}
    
    current_files = {}
    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == '.manifest.json':
                    continue
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, directory)
                
                file_hash = calculate_file_hash(filepath)
                file_size = get_file_size(filepath)
                
                if file_hash is not None and file_size is not None:
                    current_files[relative_path] = {
                        'hash': file_hash,
                        'size': file_size
                    }
    
    manifest_files = set(manifest.keys())
    current_file_set = set(current_files.keys())
    
    modified_files = []
    missing_files = []
    new_files = []
    
    for file_path in manifest_files:
        if file_path in current_files:
            if (manifest[file_path].get('hash') != current_files[file_path]['hash'] or 
                manifest[file_path].get('size') != current_files[file_path]['size']):
                modified_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    for file_path in current_file_set:
        if file_path not in manifest_files:
            new_files.append(file_path)
    
    if not modified_files and not missing_files and not new_files:
        print(f"OK {len(manifest_files)}")
    else:
        for file_path in sorted(modified_files):
            print(f"MODIFIED {file_path}")
        for file_path in sorted(missing_files):
            print(f"MISSING {file_path}")
        for file_path in sorted(new_files):
            print(f"NEW {file_path}")

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if len(lines) < 2:
        return
    
    directory = lines[0].strip()
    command = lines[1].strip()
    
    if command == 'build':
        manifest_path, file_count = build_manifest(directory)
        print(f"Manifest saved: {manifest_path} ({file_count} files)")
    
    elif command == 'check':
        if len(lines) < 3:
            manifest_path = '/tmp/manifest.json'
        else:
            manifest_path = lines[2].strip()
        check_manifest(directory, manifest_path)

if __name__ == "__main__":
    main()