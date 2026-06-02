import hashlib
import sys
import os

def compute_sha256(filepath):
    """Compute SHA-256 checksum for a file"""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except (IOError, OSError):
        return None

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        return
    
    mode = lines[0]
    
    if mode == "compute":
        # Compute mode: compute SHA-256 for each file
        for i in range(1, len(lines)):
            filepath = lines[i]
            checksum = compute_sha256(filepath)
            if checksum is not None:
                print(f"{checksum}  {filepath}")
    
    elif mode == "verify":
        # Verify mode: compare against manifest
        if len(lines) < 2:
            return
        
        manifest_path = lines[1]
        
        # Read manifest file
        manifest = {}
        try:
            with open(manifest_path, 'r') as f:
                for line in f:
                    line = line.rstrip('\n')
                    if line and '  ' in line:
                        checksum, filepath = line.split('  ', 1)
                        manifest[filepath] = checksum
        except (IOError, OSError):
            return
        
        # Verify each file
        for i in range(2, len(lines)):
            filepath = lines[i]
            current_checksum = compute_sha256(filepath)
            
            if filepath in manifest and current_checksum is not None:
                expected_checksum = manifest[filepath]
                if current_checksum == expected_checksum:
                    print(f"OK {filepath}")
                else:
                    print(f"FAIL {filepath}")
            else:
                print(f"FAIL {filepath}")

if __name__ == "__main__":
    main()