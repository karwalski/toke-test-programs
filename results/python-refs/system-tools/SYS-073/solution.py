import subprocess
import sys
import time

# Read the command from stdin
command = input().strip()

# Record start time
start_time = time.time()

# Run the command and capture output
try:
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Read output line by line and add timestamps
    for line in process.stdout:
        # Calculate elapsed time in milliseconds
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        # Remove trailing newline from line and print with timestamp
        line = line.rstrip('\n')
        print(f"[T+{elapsed_ms}ms] {line}")
    
    process.wait()
    
except Exception:
    pass