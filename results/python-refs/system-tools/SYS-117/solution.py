import os
import sys

def find_executables(prefix_filter=None):
    executables = []
    path_env = os.environ.get('PATH', '')
    
    if not path_env:
        return executables
    
    path_dirs = path_env.split(os.pathsep)
    
    for directory in path_dirs:
        if not os.path.isdir(directory):
            continue
            
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                
                # Check if it's a file and executable
                if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
                    # Apply prefix filter if provided
                    if prefix_filter is None or filename.startswith(prefix_filter):
                        executables.append(filepath)
        except (PermissionError, OSError):
            # Skip directories we can't read
            continue
    
    return sorted(list(set(executables)))

def main():
    # Read input from stdin
    input_line = sys.stdin.read().strip()
    
    # If input is empty, list all executables
    if not input_line:
        prefix_filter = None
    else:
        prefix_filter = input_line
    
    executables = find_executables(prefix_filter)
    
    # Output results
    for executable in executables:
        print(executable)

if __name__ == "__main__":
    main()