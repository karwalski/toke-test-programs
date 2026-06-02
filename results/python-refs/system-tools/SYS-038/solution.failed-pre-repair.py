import sys
import os
import time
from datetime import datetime, timezone
import threading

def main():
    # Read input
    directory = input().strip()
    duration_seconds = int(input().strip())
    
    # If duration is 0, exit immediately
    if duration_seconds == 0:
        return
    
    # Track file states
    file_states = {}
    events = []
    
    def scan_directory():
        current_files = {}
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        stat = os.stat(filepath)
                        current_files[filepath] = {
                            'mtime': stat.st_mtime,
                            'size': stat.st_size
                        }
                    except (OSError, FileNotFoundError):
                        pass
        return current_files
    
    def check_events():
        nonlocal file_states, events
        current_files = scan_directory()
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Check for new files (CREATE)
        for filepath in current_files:
            if filepath not in file_states:
                events.append(f"{now} CREATE {filepath}")
        
        # Check for deleted files (DELETE)
        for filepath in file_states:
            if filepath not in current_files:
                events.append(f"{now} DELETE {filepath}")
        
        # Check for modified files (MODIFY)
        for filepath in current_files:
            if filepath in file_states:
                old_state = file_states[filepath]
                new_state = current_files[filepath]
                if old_state['mtime'] != new_state['mtime'] or old_state['size'] != new_state['size']:
                    events.append(f"{now} MODIFY {filepath}")
        
        file_states = current_files
    
    # Initial scan
    file_states = scan_directory()
    
    # Monitor for the specified duration
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        time.sleep(0.1)  # Check every 100ms
        check_events()
    
    # Output events
    for event in events:
        print(event)

if __name__ == "__main__":
    main()