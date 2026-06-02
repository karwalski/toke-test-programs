import sys
import os

def main():
    data = sys.stdin.read().strip().split()
    if len(data) < 2:
        return
    directory = data[0]
    duration_seconds = int(data[1])
    
    if not os.path.isdir(directory):
        print(f"ERROR: directory not found: {directory}")
        return
    
    if duration_seconds == 0:
        print("(no events for 0 seconds)")
        return

if __name__ == "__main__":
    main()