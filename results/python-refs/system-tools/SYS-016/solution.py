#!/usr/bin/env python3
import os
import sys
import signal
import time
import threading

def daemon_main(pid_file, log_file, duration):
    # Write PID file
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))
    
    # Set up signal handler for clean shutdown
    def signal_handler(signum, frame):
        # Clean up PID file
        try:
            os.remove(pid_file)
        except:
            pass
        # Log shutdown
        with open(log_file, 'a') as f:
            f.write(f"Daemon shutdown signal received\n")
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Log daemon start
    with open(log_file, 'w') as f:
        f.write(f"Daemon started with PID {os.getpid()}\n")
    
    # Run for specified duration
    time.sleep(duration)
    
    # Clean shutdown
    try:
        os.remove(pid_file)
    except:
        pass
    
    with open(log_file, 'a') as f:
        f.write(f"Daemon exiting after {duration} seconds\n")

def main():
    # Read input
    pid_file = input().strip()
    log_file = input().strip()
    duration = int(input().strip())
    
    # Fork to background
    try:
        pid = os.fork()
        if pid > 0:
            # Parent process - print output and exit
            print(f"Daemon started: pid={pid}")
            return
    except OSError:
        sys.exit(1)
    
    # Child process continues as daemon
    # Detach from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)
    
    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)
    
    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Run daemon main function
    daemon_main(pid_file, log_file, duration)

if __name__ == "__main__":
    main()