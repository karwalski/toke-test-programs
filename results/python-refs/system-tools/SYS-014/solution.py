import os
import sys
import time

def main():
    temp_dir = "/tmp/managed"
    
    # Create the managed temp directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split()
        command = parts[0]
        
        if command == "CREATE":
            name = parts[1]
            filepath = os.path.join(temp_dir, name)
            # Create the file
            with open(filepath, 'w') as f:
                f.write("")
            print(filepath)
            
        elif command == "LIST":
            # List all files in the temp directory with their modification times
            try:
                files = os.listdir(temp_dir)
                for filename in sorted(files):
                    filepath = os.path.join(temp_dir, filename)
                    if os.path.isfile(filepath):
                        mtime = os.path.getmtime(filepath)
                        print(f"{filepath} {mtime}")
            except OSError:
                pass
                
        elif command == "CLEANUP":
            age_seconds = int(parts[1])
            current_time = time.time()
            removed_count = 0
            
            try:
                files = os.listdir(temp_dir)
                for filename in files:
                    filepath = os.path.join(temp_dir, filename)
                    if os.path.isfile(filepath):
                        mtime = os.path.getmtime(filepath)
                        if current_time - mtime >= age_seconds:
                            os.remove(filepath)
                            removed_count += 1
            except OSError:
                pass
                
            print(f"Removed {removed_count} files.")

if __name__ == "__main__":
    main()