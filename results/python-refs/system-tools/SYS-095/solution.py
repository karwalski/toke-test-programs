#!/usr/bin/env python3
import os
import sys
import glob
import subprocess

def get_binary_from_core(core_path):
    """Try to determine the binary that created the core dump"""
    try:
        # Try using file command to get info about core dump
        result = subprocess.run(['file', core_path], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            output = result.stdout.lower()
            # Look for executable name in file output
            if 'core file' in output or 'core dump' in output:
                # Try to extract program name from file output
                parts = output.split()
                for i, part in enumerate(parts):
                    if part == 'from' and i + 1 < len(parts):
                        return parts[i + 1].strip("'\"")
    except:
        pass
    
    # Try gdb if available
    try:
        result = subprocess.run(['gdb', '-batch', '-ex', 'info proc', '-c', core_path], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'process' in line.lower() and 'exe' in line.lower():
                    parts = line.split()
                    if len(parts) > 0:
                        return os.path.basename(parts[-1])
    except:
        pass
    
    return "unknown"

def find_core_dumps(search_dirs):
    """Find core dump files in the specified directories"""
    core_dumps = []
    
    for search_dir in search_dirs:
        if not os.path.exists(search_dir):
            continue
            
        try:
            # Common core dump patterns
            patterns = [
                os.path.join(search_dir, 'core'),
                os.path.join(search_dir, 'core.*'),
                os.path.join(search_dir, '*.core'),
                os.path.join(search_dir, 'vgcore.*'),
            ]
            
            for pattern in patterns:
                for filepath in glob.glob(pattern):
                    if os.path.isfile(filepath):
                        try:
                            size_bytes = os.path.getsize(filepath)
                            size_mb = round(size_bytes / (1024 * 1024), 1)
                            binary = get_binary_from_core(filepath)
                            core_dumps.append((filepath, size_mb, binary))
                        except:
                            continue
                            
        except:
            continue
    
    return core_dumps

def main():
    # Read input from stdin
    input_line = sys.stdin.read().strip()
    
    # Determine search directories
    if input_line:
        search_dirs = [input_line]
    else:
        search_dirs = ['.', '/tmp', '/var/crash']
    
    # Find core dumps
    core_dumps = find_core_dumps(search_dirs)
    
    if core_dumps:
        for path, size_mb, binary in core_dumps:
            print(f"{path} {size_mb} {binary}")
    else:
        print("No core dumps found")

if __name__ == "__main__":
    main()