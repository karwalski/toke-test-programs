import sys
import subprocess

# Read input
lines = sys.stdin.read().strip().split('\n')
formatter_command = lines[0].split()
file_paths = lines[1:]

# Check each file
for file_path in file_paths:
    try:
        # Run the formatter command on the file
        result = subprocess.run(formatter_command + [file_path], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        
        # For gofmt -l, it outputs the filename if formatting is needed
        # For other formatters, we check if output is empty
        if result.stdout.strip():
            print(f"NEEDS FORMAT: {file_path}")
        else:
            print(f"PASS: {file_path}")
            
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        # If command fails or times out, assume formatting is needed
        print(f"NEEDS FORMAT: {file_path}")