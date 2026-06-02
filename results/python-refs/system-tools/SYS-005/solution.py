import os
import sys
import shutil
import gzip
from datetime import datetime

def main():
    # Read input
    log_file_path = input().strip()
    compress_option = input().strip().lower()
    
    # Generate timestamp suffix
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create new path with timestamp
    new_path = f"{log_file_path}.{timestamp}"
    
    # If compression is requested, add .gz extension
    if compress_option == "yes":
        new_path += ".gz"
    
    # Check if original log file exists
    if os.path.exists(log_file_path):
        if compress_option == "yes":
            # Compress and move the file
            with open(log_file_path, 'rb') as f_in:
                with gzip.open(new_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # Remove original file after compression
            os.remove(log_file_path)
        else:
            # Just rename the file
            os.rename(log_file_path, new_path)
    
    # Create new empty log file
    open(log_file_path, 'w').close()
    
    # Output results
    print(f"Rotated to: {new_path}")
    print(f"New log created: {log_file_path}")

if __name__ == "__main__":
    main()