import subprocess
import sys
import time

# Read input
timeout_seconds = int(input().strip())
command = input().strip()

# Start the process
start_time = time.time()
try:
    # Run the command with timeout
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout_seconds
    )
    
    end_time = time.time()
    elapsed_ms = int((end_time - start_time) * 1000)
    
    # Print output from command (if any)
    if result.stdout:
        print(result.stdout.rstrip())
    
    # Print exit code and time
    print(f"exit={result.returncode} time={elapsed_ms}ms")
    
except subprocess.TimeoutExpired as e:
    end_time = time.time()
    elapsed_ms = int((end_time - start_time) * 1000)
    
    # Print any output that was captured before timeout
    if e.stdout:
        print(e.stdout.decode().rstrip())
    
    # Print timeout message
    print(f"exit=1 time={elapsed_ms}ms TIMEOUT")