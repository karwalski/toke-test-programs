import os
import time
import subprocess
import sys
from datetime import datetime

def get_file_stats(path):
    """Get modification times for all files in a directory or single file"""
    stats = {}
    if os.path.isfile(path):
        stats[path] = os.path.getmtime(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    stats[filepath] = os.path.getmtime(filepath)
                except OSError:
                    pass
    return stats

def main():
    # Read input
    path = input().strip()
    command = input().strip()
    max_triggers = int(input().strip())
    
    if not os.path.exists(path):
        return
    
    # Get initial state
    initial_stats = get_file_stats(path)
    triggers = 0
    
    # Monitor for changes
    start_time = time.time()
    while time.time() - start_time < 9:  # Run for max 9 seconds
        time.sleep(0.1)  # Check every 100ms
        
        current_stats = get_file_stats(path)
        
        # Check for changes
        changed = False
        
        # Check if any files were modified
        for filepath, mtime in current_stats.items():
            if filepath not in initial_stats or initial_stats[filepath] != mtime:
                changed = True
                break
        
        # Check if any files were deleted
        if not changed:
            for filepath in initial_stats:
                if filepath not in current_stats:
                    changed = True
                    break
        
        if changed:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Change detected: {timestamp}")
            print(f"Running: {command}")
            
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
                output = result.stdout.strip()
                print(f"Output: {output}")
            except Exception:
                print("Output: ")
            
            triggers += 1
            if max_triggers > 0 and triggers >= max_triggers:
                break
                
            # Update stats after processing change
            initial_stats = current_stats

if __name__ == "__main__":
    main()