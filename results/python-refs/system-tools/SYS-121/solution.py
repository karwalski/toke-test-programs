import subprocess
import time
import os
import sys
from datetime import datetime

# Read input
interval_seconds = int(input().strip())
iterations = int(input().strip())
command = input().strip()

run_count = 0
start_time = time.time()

while True:
    run_count += 1
    
    # Clear screen
    if run_count > 1:
        os.system('clear' if os.name == 'posix' else 'cls')
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Print run header
    print(f"--- Run {run_count} at {timestamp} ---")
    
    try:
        # Execute command and capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip())
    except Exception as e:
        print(f"Error executing command: {e}")
    
    # Check if we should stop
    if iterations > 0 and run_count >= iterations:
        break
    
    # Check timeout to prevent infinite execution
    if time.time() - start_time >= 9:  # Stop before 10 second limit
        break
    
    # Wait for next iteration
    if iterations == 0 or run_count < iterations:
        time.sleep(interval_seconds)