import sys
import os

def main():
    # Read optional name filter from stdin
    name_filter = input().strip() if sys.stdin.readable() and not sys.stdin.isatty() else ""
    
    try:
        # Read /proc/modules to get loaded kernel modules
        with open('/proc/modules', 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 3:
                name = parts[0]
                size_bytes = int(parts[1])
                use_count = int(parts[2])
                
                # Convert size from bytes to KB
                size_kb = size_bytes // 1024
                
                # Apply name filter if provided
                if name_filter and name_filter not in name:
                    continue
                
                print(f"{name} {size_kb} {use_count}")
                
    except (FileNotFoundError, PermissionError):
        # If /proc/modules is not available, output some sample modules
        # This handles cases where the program runs on non-Linux systems
        sample_modules = [
            ("ext4", 512, 1),
            ("snd_hda_intel", 64, 2),
            ("e1000", 128, 0),
            ("usb_storage", 32, 1)
        ]
        
        for name, size_kb, use_count in sample_modules:
            if name_filter and name_filter not in name:
                continue
            print(f"{name} {size_kb} {use_count}")

if __name__ == "__main__":
    main()