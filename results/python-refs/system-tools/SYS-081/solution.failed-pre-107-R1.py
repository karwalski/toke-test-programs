import sys
import time
import os

# Read input
file_path = input().strip()
n_lines = int(input().strip())
follow_duration = int(input().strip())

def get_last_n_lines(file_path, n):
    """Get the last N lines of a file efficiently"""
    try:
        with open(file_path, 'rb') as f:
            # Go to end of file
            f.seek(0, 2)
            file_size = f.tell()
            
            if file_size == 0:
                return []
            
            # Start from end and work backwards
            lines = []
            buffer_size = 8192
            buffer = b''
            position = file_size
            
            while len(lines) < n and position > 0:
                # Read a chunk
                read_size = min(buffer_size, position)
                position -= read_size
                f.seek(position)
                chunk = f.read(read_size)
                
                # Prepend to buffer
                buffer = chunk + buffer
                
                # Split into lines
                all_lines = buffer.split(b'\n')
                
                # Keep the incomplete first line for next iteration
                if position > 0:
                    buffer = all_lines[0]
                    lines_to_add = all_lines[1:]
                else:
                    buffer = b''
                    lines_to_add = all_lines
                
                # Add lines to the beginning of our list
                for line in reversed(lines_to_add):
                    if line or len(lines) == 0 or position == 0:  # Keep empty lines except trailing newline
                        lines.insert(0, line.decode('utf-8', errors='replace'))
                        if len(lines) >= n:
                            break
            
            # Remove the last empty line if it exists (from trailing newline)
            if lines and lines[-1] == '' and file_size > 0:
                with open(file_path, 'rb') as f2:
                    f2.seek(-1, 2)
                    if f2.read(1) == b'\n':
                        lines = lines[:-1]
            
            return lines[-n:] if len(lines) > n else lines
            
    except (FileNotFoundError, PermissionError, IOError):
        return []

# Print last N lines
last_lines = get_last_n_lines(file_path, n_lines)
for line in last_lines:
    print(line)

# Follow file if duration > 0
if follow_duration > 0:
    try:
        start_time = time.time()
        # Get initial file size
        initial_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            # Seek to end
            f.seek(0, 2)
            
            while time.time() - start_time < follow_duration:
                # Check for new content
                line = f.readline()
                if line:
                    # Remove trailing newline for consistent output
                    print(line.rstrip('\n\r'))
                else:
                    # No new content, sleep briefly
                    time.sleep(0.1)
                    
    except (FileNotFoundError, PermissionError, IOError):
        pass