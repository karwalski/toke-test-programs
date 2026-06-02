import os
import sys

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

pid_file_path = lines[0]
command = lines[1]

if command == "start":
    # Get current process PID
    current_pid = os.getpid()
    
    # Write PID to file
    with open(pid_file_path, 'w') as f:
        f.write(str(current_pid))
    
    print(f"PID written: {current_pid}")

elif command == "check":
    # Check if PID file exists and read it
    if os.path.exists(pid_file_path):
        try:
            with open(pid_file_path, 'r') as f:
                pid = f.read().strip()
            print(f"RUNNING pid={pid}")
        except:
            print("NOT_RUNNING")
    else:
        print("NOT_RUNNING")

elif command == "stop":
    # Remove PID file if it exists
    if os.path.exists(pid_file_path):
        os.remove(pid_file_path)
    print("PID file removed")