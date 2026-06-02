import subprocess
import signal
import sys
import os
import time
from datetime import datetime

def signal_handler(signum, frame):
    global child_process, signals_received
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sig_name = signal.Signals(signum).name
    print(f"Signal {sig_name} received at {timestamp}")
    signals_received.append((signum, timestamp))
    
    if child_process and child_process.poll() is None:
        try:
            child_process.send_signal(signum)
        except ProcessLookupError:
            pass

def main():
    global child_process, signals_received
    child_process = None
    signals_received = []
    
    # Read command from stdin
    command = input().strip()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    
    try:
        # Start child process
        child_process = subprocess.Popen(command.split())
        print(f"Child started: {child_process.pid}")
        
        # Wait for child to complete
        exit_code = child_process.wait()
        
        print(f"Child exited: code={exit_code}")
        
    except Exception as e:
        if child_process:
            try:
                child_process.terminate()
                child_process.wait()
            except:
                pass
        sys.exit(1)

if __name__ == "__main__":
    main()