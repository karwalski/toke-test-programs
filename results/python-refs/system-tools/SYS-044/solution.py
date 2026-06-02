import os
import sys
import time
from datetime import datetime, timedelta

def format_age(seconds):
    """Convert seconds to human-readable format"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes}m"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours}h"
    else:
        days = int(seconds / 86400)
        return f"{days}d"

def main():
    # Read input
    directory = input().strip()
    stale_threshold_hours = int(input().strip())
    
    current_time = time.time()
    stale_threshold_seconds = stale_threshold_hours * 3600
    
    try:
        # Get all files in directory
        files = []
        for item in os.listdir(directory):
            filepath = os.path.join(directory, item)
            if os.path.isfile(filepath):
                files.append(filepath)
        
        # Sort files by name for consistent output
        files.sort()
        
        for filepath in files:
            try:
                # Get modification time
                mod_time = os.path.getmtime(filepath)
                age_seconds = current_time - mod_time
                
                # Format age
                age_str = format_age(age_seconds)
                
                # Check if stale
                stale_marker = " [STALE]" if age_seconds > stale_threshold_seconds else ""
                
                print(f"{filepath}: {age_str}{stale_marker}")
                
            except (OSError, IOError):
                # Skip files we can't access
                continue
                
    except (OSError, IOError):
        # Directory doesn't exist or can't be accessed
        pass

if __name__ == "__main__":
    main()