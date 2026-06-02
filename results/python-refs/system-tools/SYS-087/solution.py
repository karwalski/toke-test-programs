import os
import stat
import sys

def parse_octal_mode(mode_str):
    """Convert octal string to integer mode"""
    return int(mode_str, 8)

def get_current_mode(path):
    """Get current file mode (permissions only)"""
    return stat.S_IMODE(os.stat(path).st_mode)

def fix_permissions(directory, file_mode, dir_mode, dry_run):
    """Recursively fix file permissions"""
    changes = []
    
    for root, dirs, files in os.walk(directory):
        # Check directory permissions
        current_mode = get_current_mode(root)
        if current_mode != dir_mode:
            mode_str = oct(dir_mode)[2:]  # Remove '0o' prefix
            changes.append(f"chmod {mode_str} {root}")
            if not dry_run:
                os.chmod(root, dir_mode)
        
        # Check file permissions
        for file in files:
            file_path = os.path.join(root, file)
            try:
                current_mode = get_current_mode(file_path)
                if current_mode != file_mode:
                    mode_str = oct(file_mode)[2:]  # Remove '0o' prefix
                    changes.append(f"chmod {mode_str} {file_path}")
                    if not dry_run:
                        os.chmod(file_path, file_mode)
            except (OSError, IOError):
                # Skip files we can't access
                continue
    
    return changes

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    directory = lines[0]
    file_mode = parse_octal_mode(lines[1]) if len(lines) > 1 and lines[1] else 0o644
    dir_mode = parse_octal_mode(lines[2]) if len(lines) > 2 and lines[2] else 0o755
    dry_run = lines[3].lower() == "yes" if len(lines) > 3 else True
    
    try:
        changes = fix_permissions(directory, file_mode, dir_mode, dry_run)
        
        # Print changes
        for change in changes:
            print(change)
        
        # Print summary
        print(f"Summary: {len(changes)} files changed.")
        
    except Exception:
        # If directory doesn't exist or other errors, show no changes
        print("Summary: 0 files changed.")

if __name__ == "__main__":
    main()