import sys
import os
import time
from datetime import datetime
import threading

def watch_directory(directory, duration):
    if duration == 0:
        return
    
    # Store initial state of directory
    initial_files = {}
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    stat = os.stat(filepath)
                    initial_files[filepath] = stat.st_mtime
                except OSError:
                    pass
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        current_files = {}
        
        # Get current state
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        stat = os.stat(filepath)
                        current_files[filepath] = stat.st_mtime
                    except OSError:
                        pass
        
        # Check for new files (CREATED)
        for filepath in current_files:
            if filepath not in initial_files:
                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                print(f"{timestamp} CREATED {filepath}")
        
        # Check for modified files (MODIFIED)
        for filepath in current_files:
            if filepath in initial_files and current_files[filepath] != initial_files[filepath]:
                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                print(f"{timestamp} MODIFIED {filepath}")
        
        # Check for deleted files (DELETED)
        for filepath in initial_files:
            if filepath not in current_files:
                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                print(f"{timestamp} DELETED {filepath}")
        
        # Update initial_files for next iteration
        initial_files = current_files.copy()
        
        # Sleep briefly to avoid excessive CPU usage
        time.sleep(0.1)

# Read input
line = input().strip()
parts = line.split()
directory = parts[0]
duration = int(parts[1]) if len(parts) > 1 else 5

# Watch directory
watch_directory(directory, duration)