import os
import sys
import signal
import time

def get_terminal_size():
    try:
        rows, cols = os.get_terminal_size()
        return rows, cols
    except OSError:
        # Fallback if terminal size cannot be determined
        return 24, 80

def print_size(rows, cols):
    print(f"Rows: {rows} Cols: {cols}")

def signal_handler(signum, frame):
    rows, cols = get_terminal_size()
    print_size(rows, cols)

def main():
    watch_duration = int(input().strip())
    
    # Report current size
    rows, cols = get_terminal_size()
    print_size(rows, cols)
    
    if watch_duration > 0:
        # Set up signal handler for window resize
        signal.signal(signal.SIGWINCH, signal_handler)
        
        # Watch for resize events
        start_time = time.time()
        last_size = (rows, cols)
        
        while time.time() - start_time < watch_duration:
            current_size = get_terminal_size()
            if current_size != last_size:
                print_size(current_size[0], current_size[1])
                last_size = current_size
            time.sleep(0.1)  # Small delay to avoid busy waiting

if __name__ == "__main__":
    main()